from utils.subsystembase import SubsystemBase

import commands2
import wpilib
from wpimath.controller import SimpleMotorFeedforwardMeters, BangBangController
import rev
from wpilib import RobotBase, RobotController
from utils.sparkmaxsim import SparkMaxSim
from wpilib.simulation import FlywheelSim
from wpimath.system.plant import DCMotor
from utils.linearInterpolator import LinearInterpolator
import properties

import ports


def compute_speed_percentage(speed, setpoint):
    if setpoint <= 0.0:
        return 0
    else:
        return round(min(100.0, speed / setpoint * 100))

class Shooter(commands2.SubsystemBase):
    main_verified_points = [[-1, 100], [0, 1000], [0.5, 2500], [1, 3000]]
    backspin_verified_points = [[-1, 100], [0, 1000], [0.5, 2500], [1, 3000]]
    main_interpolator = LinearInterpolator(main_verified_points)
    backspin_interpolator = LinearInterpolator(backspin_verified_points)

    def __init__(self) -> None:
        super().__init__()
        self._motor_left = rev.CANSparkMax(ports.shooter_motor_gauche, rev.CANSparkMax.MotorType.kBrushless)
        self._motor_left.restoreFactoryDefaults()
        self._motor_left.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self._motor_right = rev.CANSparkMax(ports.shooter_motor_droit, rev.CANSparkMax.MotorType.kBrushless)
        self._motor_right.restoreFactoryDefaults()
        self._motor_right.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self._motor_right.follow(self._motor_left, invert=True)

        self._backspin_motor = rev.CANSparkMax(ports.shooter_backspin_motor, rev.CANSparkMax.MotorType.kBrushless)
        self._backspin_motor.restoreFactoryDefaults()
        self._backspin_motor.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.backspin_encoder = self._backspin_motor.getEncoder()
        self.encoder = self._motor_left.getEncoder()

        self.bang_bang_controller = BangBangController()
        self.feed_forward_controller = SimpleMotorFeedforwardMeters()

        self.setpoint = 1
        self.backspin_setpoint = 1

        if RobotBase.isSimulation():
            self.motor_left_sim = SparkMaxSim(self._motor_left)
            self.flywheel_sim = FlywheelSim(DCMotor.NEO(2), 1, 0.0025)

            self.backspin_motor_sim = SparkMaxSim(self._backspin_motor)
            self.backspin_flywheel_sim = FlywheelSim(DCMotor.NEO(1), 1, 0.0025)

    def shoot(self, setpoint: float, backspin_setpoint):
        self._motor_left.set(self.bang_bang_controller.calculate(self.encoder.getVelocity(), setpoint)
                             + 0.9 * self.feed_forward_controller.calculate(setpoint))
        self._backspin_motor.set(
            self.bang_bang_controller.calculate(self.backspin_encoder.getVelocity(), backspin_setpoint)
            + 0.9 * self.feed_forward_controller.calculate(backspin_setpoint))
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def shoot_at_height(self, height):
        self.shoot(self.main_interpolator.interpolate(height), self.backspin_interpolator.interpolate(height))

    def disable(self):
        self._motor_left.set(0)
        self._backspin_motor.set(0)
        self.setpoint = 0
        self.backspin_setpoint = 0

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("BackspinMotor", self.backspin_encoder.getVelocity())
        wpilib.SmartDashboard.putNumber("MainMotors", self.encoder.getVelocity())

        wpilib.SmartDashboard.putNumber("MainMotorPercentSpeed", compute_speed_percentage(self.encoder.getVelocity(), self.setpoint))
        wpilib.SmartDashboard.putNumber("BackspinMotorPercentSpeed", compute_speed_percentage(self.backspin_encoder.getVelocity(), self.backspin_setpoint))



    def simulationPeriodic(self) -> None:
        motor_value = self._motor_left.get()
        self.flywheel_sim.setInputVoltage(motor_value * RobotController.getInputVoltage())
        self.flywheel_sim.update(0.02)
        self.motor_left_sim.setVelocity(self.flywheel_sim.getAngularVelocity() / 6.28 * 60)
        backspin_motor_value = self._backspin_motor.get()
        self.backspin_flywheel_sim.setInputVoltage(backspin_motor_value * RobotController.getInputVoltage())
        self.backspin_flywheel_sim.update(0.02)
        self.backspin_motor_sim.setVelocity(self.backspin_flywheel_sim.getAngularVelocity() / 6.28 * 60)
        # self.motor_right_sim.setVelocity(self.bang_bang_controller.calculate(self._encoder_primaire.getVelocity(), setpoint)
        #                     + 0.9 * self.feed_forward_controller.calculate(setpoint))
        # self.motor_left_sim.setVelocity(self.bang_bang_controller.calculate(self._encoder_primaire.getVelocity(), setpoint)
        #                     + 0.9 * self.feed_forward_controller.calculate(setpoint))

