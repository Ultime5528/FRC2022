import wpimath.controller
import commands2
import rev

class Shooter(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.shooter_motor_left = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.shooter_motor_left = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.bang_bang_controller = wpimath.controller.BangBangController()
