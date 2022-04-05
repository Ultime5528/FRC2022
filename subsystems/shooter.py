import commands2
import rev
import wpilib
from wpilib import RobotBase, RobotController
from wpilib.simulation import FlywheelSim
from wpimath.controller import SimpleMotorFeedforwardMeters, BangBangController, PIDController
from wpimath.system.plant import DCMotor

import ports
import properties
from utils.linearinterpolator import LinearInterpolator
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutil import configure_leader, configure_follower


def compute_speed_percentage(speed, setpoint):
    if setpoint <= 0.0:
        return 0
    else:
        return round(min(100.0, speed / setpoint * 100))


class Shooter(commands2.SubsystemBase):
    # main_verified_points = [[0.1, 2500], [0.15, 2500], [0.2, 2600], [0.333, 2700], [0.4, 2800], [0.56, 2900], [0.64, 4300], [0.7, 4500]]
    # backspin_verified_points = main_verified_points
    main_verified_points = [(-0.4, 1200), (-0.3, 1200), (0, 1400), (0.16, 3750), (0.43, 4100), (0.65, 4750)]
    backspin_verified_points = [(-0.4, 3300), (-0.3, 3600), (0, 3600), (0.16, 1600), (0.43, 2000), (0.65, 2400)]
    main_interpolator = LinearInterpolator(main_verified_points)
    backspin_interpolator = LinearInterpolator(backspin_verified_points)

    def __init__(self) -> None:
        super().__init__()
        self._motor_left = rev.CANSparkMax(ports.shooter_motor_gauche, rev.CANSparkMax.MotorType.kBrushless)
        configure_leader(self._motor_left, "coast", inverted=True)

        self._motor_right = rev.CANSparkMax(ports.shooter_motor_droit, rev.CANSparkMax.MotorType.kBrushless)
        configure_follower(self._motor_right, self._motor_left, "coast", inverted=True)

        self._backspin_motor = rev.CANSparkMax(ports.shooter_backspin_motor, rev.CANSparkMax.MotorType.kBrushless)
        configure_leader(self._backspin_motor, "coast", inverted=True)

        self.encoder = self._motor_left.getEncoder()
        self.backspin_encoder = self._backspin_motor.getEncoder()

        self.pid_controller = PIDController(0.0001, 0, 0)
        self.addChild("PID Controller", self.pid_controller)
        self.bang_bang_controller = BangBangController()
        self.feed_forward_controller = SimpleMotorFeedforwardMeters(0.124, 0.002105)

        self.setpoint = 1
        self.backspin_setpoint = 1

        if RobotBase.isSimulation():
            self.motor_left_sim = SparkMaxSim(self._motor_left)
            self.flywheel_sim = FlywheelSim(DCMotor.NEO(2), 1, 0.0025)

            self.backspin_motor_sim = SparkMaxSim(self._backspin_motor)
            self.backspin_flywheel_sim = FlywheelSim(DCMotor.NEO(1), 1, 0.0025)

    def shoot(self, setpoint: float, backspin_setpoint):
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

        # Main motor control
        velocity = self.encoder.getVelocity()
        pid_value = self.pid_controller.calculate(velocity, setpoint)
        feedforward_value = self.feed_forward_controller.calculate(setpoint)
        voltage = pid_value + feedforward_value
        self._motor_left.setVoltage(voltage)

        # print("\n---------------------")
        # print("Setpoint:", setpoint)
        # print("Velocity: ", velocity)
        # print("PID Value: ", pid_value)
        # print("Feedforward Value: ", feedforward_value)
        # print("Voltage: ", voltage)

        # Backspin motor control
        self._backspin_motor.setVoltage(
            self.pid_controller.calculate(self.backspin_encoder.getVelocity(), backspin_setpoint)
            + self.feed_forward_controller.calculate(backspin_setpoint)
        )

    def shoot_bangbang(self, setpoint: float, backspin_setpoint):
        velocity = self.encoder.getVelocity()
        bangbang_value = self.bang_bang_controller.calculate(velocity, setpoint)
        feedforward_value = self.feed_forward_controller.calculate(setpoint)
        voltage = bangbang_value + 0.95 * feedforward_value
        self._motor_left.setVoltage(voltage)
        # print("\n---------------------")
        # print("Setpoint:", setpoint)
        # print("Velocity: ", velocity)
        # print("Bang Bang Value: ", bangbang_value)
        # print("Feedforward Value: ", feedforward_value)
        # print("Voltage: ", voltage)

        self._backspin_motor.setVoltage(
            self.bang_bang_controller.calculate(self.backspin_encoder.getVelocity(), backspin_setpoint)
            + properties.values.shooter_feedforward_percentage
            * self.feed_forward_controller.calculate(backspin_setpoint)
        )

        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def atSetpoint(self):
        if self.setpoint:
            return (
                    self.encoder.getVelocity() >= self.setpoint - properties.values.shooter_tolerance
                    and self.backspin_encoder.getVelocity() >= self.backspin_setpoint - properties.values.shooter_tolerance
            )
        else:
            return False

    def shoot_at_height(self, height):
        self.shoot(
            self.main_interpolator.interpolate(height),
            self.backspin_interpolator.interpolate(height),
        )

    def stop(self):
        self._motor_left.set(0)
        self._backspin_motor.set(0)
        self.setpoint = 0
        self.backspin_setpoint = 0

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("BackspinMotor", self.backspin_encoder.getVelocity())
        wpilib.SmartDashboard.putNumber("MainMotors", self.encoder.getVelocity())

        wpilib.SmartDashboard.putNumber(
            "MainMotorPercentSpeed",
            compute_speed_percentage(self.encoder.getVelocity(), self.setpoint),
        )
        wpilib.SmartDashboard.putNumber(
            "BackspinMotorPercentSpeed",
            compute_speed_percentage(self.backspin_encoder.getVelocity(), self.backspin_setpoint),
        )

    def simulationPeriodic(self) -> None:
        motor_value = self._motor_left.get()
        self.flywheel_sim.setInputVoltage(motor_value * RobotController.getInputVoltage())
        self.flywheel_sim.update(0.02)
        self.motor_left_sim.setVelocity(self.flywheel_sim.getAngularVelocity() / 6.28 * 60)
        backspin_motor_value = self._backspin_motor.get()
        self.backspin_flywheel_sim.setInputVoltage(backspin_motor_value * RobotController.getInputVoltage())
        self.backspin_flywheel_sim.update(0.02)
        self.backspin_motor_sim.setVelocity(self.backspin_flywheel_sim.getAngularVelocity() / 6.28 * 60)
