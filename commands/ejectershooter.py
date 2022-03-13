import commands2
from subsystems.shooter import Shooter
import wpilib
from properties import values


class EjecterShooter(commands2.CommandBase):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.timer = wpilib.Timer()
        self.setName("Ejecter Shooter")

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.shooter.shoot(values.shooter_ejecter_speed, values.shooter_ejecter_backspin_speed)

    def isFinished(self) -> bool:
        return self.timer.get() >= values.shooter_ejecter_temps

    def end(self, interrupted: bool) -> None:
        self.timer.stop()
        self.shooter.disable()
