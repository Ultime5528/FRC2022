import commands2
from wpimath.controller import SimpleMotorFeedforwardMeters, BangBangController
import rev


class Shooter(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        self.motor_left = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right.follow(self.motor_left, invert=True)
        self.encoder = self.motor_left.getEncoder()
        self.bang_bang_controller = BangBangController()
        self.feed_forward_controller = SimpleMotorFeedforwardMeters()

    def shoot(self, setpoint):
        self.motor_left.set(self.bang_bang_controller.calculate(self.encoder.getVelocity(), setpoint)
                            + 0.9 * self.feed_forward_controller.calculate(setpoint))
