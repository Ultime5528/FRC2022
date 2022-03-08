import wpilib
from commands2 import CommandBase

import properties
from subsystems.intake import Intake


class EjecterIntake(CommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.setName("Ejecter Intake")
        self.timer = wpilib.Timer()
        self.intake = intake

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.intake.ejecter()

    def end(self, interrupted: bool) -> None:
        self.intake.stopIntake()
        self.intake.stopTransporter()

    def isFinished(self) -> bool:
        return self.timer.get() >= properties.values.intake_duree_ejection
