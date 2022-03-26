import commands2

from commands.descendreintake import DescendreIntake
from commands.monterintake import MonterIntake
from commands.prendreballon import PrendreBallon
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake


class SequencePrendre(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire, intake: Intake):
        super().__init__(
            commands2.ParallelCommandGroup(
                DescendreIntake(grimpeur_secondaire),
                PrendreBallon(intake),
            ),
            MonterIntake(grimpeur_secondaire),
        )
        self.setName("Sequence Prendre")
