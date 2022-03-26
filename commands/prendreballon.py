from commands2 import CommandBase
from subsystems.intake import Intake


class PrendreBallon(CommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(self.intake)
        self.setName("Prendre Ballon")

    def execute(self):
        self.intake.activerIntake()

        if self.intake.hasBallConvoyeur():
            self.intake.stopConvoyeur()
        else:
            self.intake.activerConvoyeur()

    def isFinished(self) -> bool:
        return self.intake.hasBallIntake() and self.intake.hasBallConvoyeur()

    def end(self, interrupted: bool) -> None:
        self.intake.stopIntake()
        self.intake.stopConvoyeur()
