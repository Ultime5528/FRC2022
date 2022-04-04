import commands2

from commands.balayerballon import BalayerBallon
from commands.intake.descendreintake import DescendreIntake
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake


class SequenceBalayer(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire, intake: Intake):
        super().__init__(
            DescendreIntake(grimpeur_secondaire),
            BalayerBallon(intake),
        )
        self.setName(self.__class__.__name__)
