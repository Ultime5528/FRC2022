from commands2 import CommandBase
import wpilib
from subsystems.intake import Intake


class PrendreBallon(CommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(self.intake)
        self.setName("PrendreBallon")

    def execute(self):
        self.intake.activerIntake()

        if self.intake.hasBallTransporter():
            self.intake.stopTransporter()
        else:
            self.intake.activerTransporter()

    def isFinished(self) -> bool:
        return self.intake.hasBallIntake() and self.intake.hasBallTransporter()

    def end(self, interrupted: bool) -> None:
        self.intake.stopIntake()
        self.intake.stopTransporter()
