from commands2 import CommandBase
import wpilib
from subsystems.intake import Intake


class PrendreBallon(CommandBase):
    def __init__(self, p_intake: Intake):
        CommandBase.__init__(self)
        self.intake = p_intake
        self.addRequirements(self.intake)
        # self.setName("")

    def execute(self):
        self.intake.intakeMotor.set(1)

    def end(self, interrupted: bool) -> None:
        self.intake.intakeMotor.set(0)
