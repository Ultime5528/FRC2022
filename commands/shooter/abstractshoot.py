import wpilib

import properties
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from utils.safecommandbase import SafeCommandBase


class AbstractShoot(SafeCommandBase):
    def __init__(self, shooter: Shooter, intake: Intake):
        super().__init__()
        self.shooter = shooter
        self.intake = intake
        self.addRequirements(self.shooter, self.intake)
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()

    def shoot(self):
        raise NotImplementedError("Doit être overridé dans une sous-classe")

    def execute(self) -> None:
        self.shoot()

        if self.shooter.atSetpoint():
            self.intake.activerConvoyeurRapide()
        else:
            self.intake.stopConvoyeur()

        if not self.intake.hasBallIntake() and not self.intake.hasBallConvoyeur():
            self.timer.start()
        else:
            self.timer.stop()
            self.timer.reset()

    def isFinished(self) -> bool:
        return self.timer.get() >= properties.values.shooter_end_time

    def end(self, interrupted: bool) -> None:
        self.shooter.stop()
        self.intake.stopConvoyeur()
