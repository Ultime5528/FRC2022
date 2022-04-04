from subsystems.intake import Intake
from utils.safecommandbase import SafeCommandBase


class PrendreBallon(SafeCommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(self.intake)

    def execute(self):
        self.intake.activerIntake()

        if self.intake.hasBallConvoyeur():
            self.intake.stopConvoyeur()
        else:
            self.intake.activerConvoyeurLent()

    def isFinished(self) -> bool:
        return self.intake.hasBallIntake() and self.intake.hasBallConvoyeur()

    def end(self, interrupted: bool) -> None:
        self.intake.stopIntake()
        self.intake.stopConvoyeur()
