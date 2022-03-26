from commands2 import CommandBase
from subsystems.intake import Intake


class ArreterIntake(CommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)
        self.setName("ArreterIntake")

    def execute(self) -> None:
        self.intake.stopIntake()
        self.intake.stopConvoyeur()

    def isFinished(self) -> bool:
        return True
