import commands2
from subsystems.shooter import Shooter
import wpilib
from properties import values


class EjecterBallonShooter(commands2.CommandBase):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.shooter.motor_left.set(0.25)

    def isFinished(self) -> bool:
        return self.timer.get() >= values.ejecter_ballon_temps

    def end(self, interrupted: bool) -> None:
        self.timer.stop()
        self.shooter.motor_left.set(0)