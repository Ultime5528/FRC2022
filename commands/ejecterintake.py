import wpilib
from commands2 import CommandBase

from subsystems.intake import Intake


class EjecterIntake(CommandBase):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.setName("EjecterIntake")
        self.timer = wpilib.Timer()
        self.intake = intake

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.intake.intakeMotor.set(-1)
        self.intake.transporterMotor.set(-1)

    def end(self, interrupted: bool) -> None:
        self.intake.intakeMotor.set(0)
        self.intake.transporterMotor.set(0)

    def isFinished(self) -> bool:
        return self.timer.get() >= 1.5  # TODO Trouver temps adéquat
