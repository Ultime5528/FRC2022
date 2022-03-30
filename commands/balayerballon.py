import wpilib

import properties
from subsystems.intake import Intake
from utils.safecommandbase import SafeCommandBase


class BalayerBallon(SafeCommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.intake.ejecter()

    def end(self, interrupted: bool) -> None:
        self.intake.stopIntake()

    def isFinished(self) -> bool:
        return self.timer.get() >= properties.values.intake_duree_ejection
