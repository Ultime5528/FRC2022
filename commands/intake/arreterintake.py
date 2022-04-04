
from subsystems.intake import Intake
from utils.safecommandbase import SafeCommandBase


class ArreterIntake(SafeCommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)

    def execute(self) -> None:
        self.intake.stopIntake()
        self.intake.stopConvoyeur()

    def isFinished(self) -> bool:
        return True
