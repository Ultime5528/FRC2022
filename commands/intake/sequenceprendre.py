import commands2

from commands.intake.descendreintake import DescendreIntake
from commands.intake.monterintake import MonterIntake
from commands.intake.prendreballon import PrendreBallon
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake


class SequencePrendre(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire, intake: Intake):
        super().__init__(
            commands2.ParallelCommandGroup(
                DescendreIntake(grimpeur_secondaire),
                PrendreBallon(intake),
            ),
            MonterIntake(grimpeur_secondaire, intake),
        )
        self.setName(self.__class__.__name__)
