import commands2
import wpilib
from wpimath.controller import SimpleMotorFeedforwardMeters, BangBangController
import rev
from wpilib import RobotBase, RobotController
from utils.sparkmaxsim import SparkMaxSim
from wpilib.simulation import FlywheelSim
from wpimath.system.plant import DCMotor
from utils.linearInterpolator import  LinearInterpolator
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
        self.motor_left = rev.CANSparkMax(ports.shooter_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right = rev.CANSparkMax(ports.shooter_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right.follow(self.motor_left, invert=True)
        self.backspin_motor = rev.CANSparkMax(ports.shooter_backspin_motor, rev.CANSparkMax.MotorType.kBrushless)

        self.backspin_encoder = self.backspin_motor.getEncoder()
        self.encoder = self.motor_left.getEncoder()

        self.bang_bang_controller = BangBangController()
        self.feed_forward_controller = SimpleMotorFeedforwardMeters()

        self.setpoint = 1
        self.backspin_setpoint = 1

        if RobotBase.isSimulation():
            self.motor_left_sim = SparkMaxSim(self.motor_left)
            self.flywheel_sim = FlywheelSim(DCMotor.NEO(2), 1, 0.0025)

            self.backspin_motor_sim = SparkMaxSim(self.backspin_motor)
            self.backspin_flywheel_sim = FlywheelSim(DCMotor.NEO(1), 1, 0.0025)

    def shoot(self, setpoint, backspin_setpoint):
        self.motor_left.set(self.bang_bang_controller.calculate(self.encoder.getVelocity(), setpoint)
                            + 0.9 * self.feed_forward_controller.calculate(setpoint))
        self.backspin_motor.set(
            self.bang_bang_controller.calculate(self.backspin_encoder.getVelocity(), backspin_setpoint)
            + 0.9 * self.feed_forward_controller.calculate(backspin_setpoint))
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def shoot_at_height(self, height):
        self.shoot(self.main_interpolator.interpolate(height), self.backspin_interpolator.interpolate(height))

    def disable(self):
        self.motor_left.set(0)
        self.backspin_motor.set(0)
        self.setpoint = 0
        self.backspin_setpoint = 0

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Backspin Motor", self.backspin_encoder.getVelocity())
        wpilib.SmartDashboard.putNumber("Main Motors", self.encoder.getVelocity())

        wpilib.SmartDashboard.putNumber("Main Motor percent speed", compute_speed_percentage(self.encoder.getVelocity(), self.setpoint))
        wpilib.SmartDashboard.putNumber("Backspin Motor percent speed", compute_speed_percentage(self.backspin_encoder.getVelocity(), self.backspin_setpoint))



    def simulationPeriodic(self) -> None:
        motor_value = self.motor_left.get()
        self.flywheel_sim.setInputVoltage(motor_value * RobotController.getInputVoltage())
        self.flywheel_sim.update(0.02)
        self.motor_left_sim.setVelocity(self.flywheel_sim.getAngularVelocity() / 6.28 * 60)
        backspin_motor_value = self.backspin_motor.get()
        self.backspin_flywheel_sim.setInputVoltage(backspin_motor_value * RobotController.getInputVoltage())
        self.backspin_flywheel_sim.update(0.02)
        self.backspin_motor_sim.setVelocity(self.backspin_flywheel_sim.getAngularVelocity() / 6.28 * 60)
        # self.motor_right_sim.setVelocity(self.bang_bang_controller.calculate(self.encoder.getVelocity(), setpoint)
        #                     + 0.9 * self.feed_forward_controller.calculate(setpoint))
        # self.motor_left_sim.setVelocity(self.bang_bang_controller.calculate(self.encoder.getVelocity(), setpoint)
        #                     + 0.9 * self.feed_forward_controller.calculate(setpoint))

