import commands2
from wpimath.controller import SimpleMotorFeedforwardMeters, BangBangController
import rev
from wpilib import RobotBase, RobotController
from utils.sparkmaxsim import SparkMaxSim
from wpilib.simulation import FlywheelSim
from wpimath.system.plant import DCMotor


class Shooter(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        self.motor_left = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right.follow(self.motor_left, invert=True)
        self.backspin_motor = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)

        self.backspin_encoder = self.backspin_motor.getEncoder()
        self.encoder = self.motor_left.getEncoder()

        self.bang_bang_controller = BangBangController()
        self.feed_forward_controller = SimpleMotorFeedforwardMeters()

        if RobotBase.isSimulation():
            self.motor_left_sim = SparkMaxSim(self.motor_left)
            self.flywheel_sim = FlywheelSim(DCMotor.NEO(2), 1, 0.0025)

            self.backspin_motor_sim = SparkMaxSim(self.backspin_motor)
            self.backspin_flywheel_sim = FlywheelSim(DCMotor.NEO(1), 1, 0.0025)




    def shoot(self, setpoint, backspin_setpoint):
        self.motor_left.set(self.bang_bang_controller.calculate(self.encoder.getVelocity(), setpoint)
                            + 0.9 * self.feed_forward_controller.calculate(setpoint))
        self.backspin_motor.set(self.bang_bang_controller.calculate(self.backspin_encoder.getVelocity(), backspin_setpoint)
                                + 0.9 * self.feed_forward_controller.calculate(backspin_setpoint))

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

