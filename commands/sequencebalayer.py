import commands2

from commands.descendreintake import DescendreIntake
from commands.monterintake import MonterIntake
from commands.balayerballon import BalayerBallon
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake


class SequenceBalayer(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire, intake: Intake):
        super().__init__(
            DescendreIntake(grimpeur_secondaire),
            BalayerBallon(intake),
            MonterIntake(grimpeur_secondaire),
        )
        self.setName("Sequence Balayer")
