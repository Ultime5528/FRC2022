import wpilib
import commands2
from subsystems.shooter import Shooter


class Shoot(commands2.CommandBase):
    def __init__(self, shooter: Shooter, stick: wpilib.Joystick, setpoint, backspin_setpoint):
        super().__init__()

        self.stick = stick
        self.shooter = shooter
        self.addRequirements(self.shooter)
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def execute(self) -> None:
        self.shooter.shoot(self.setpoint, self.backspin_setpoint)

    def end(self, interrupted: bool) -> None:
        self.shooter.motor_left.set(0)
        self.shooter.backspin_motor.set(0)
