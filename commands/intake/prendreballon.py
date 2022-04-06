import wpilib
from commands2 import CommandBase

import properties
from subsystems.intake import Intake


class PrendreBallon(CommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(self.intake)
        self.setName("Prendre Ballon")
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.stop()
        self.timer.reset()

    def execute(self):
        self.intake.activerIntake()
        if self.intake.hasBallConvoyeur():
            if self.timer.get() < properties.values.intake_convoyeur_inertia_time:
                self.timer.start()
                self.intake.cancelInertia()
            else:
                self.intake.stopConvoyeur()
        else:
            self.intake.activerConvoyeurLent()
            self.timer.reset()

    def isFinished(self) -> bool:
        return self.intake.hasBallIntake() and self.intake.hasBallConvoyeur()

    def end(self, interrupted: bool) -> None:
        self.intake.stopIntake()
        self.intake.stopConvoyeur()
