import commands2

from commands.descendreintake import DescendreIntake
from commands.monterintake import MonterIntake
from commands.prendreballon import PrendreBallon
from subsystems.grimpeur import Grimpeur
from subsystems.intake import Intake


class SequencePrendre(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur, intake: Intake):
        super().__init__(
            DescendreIntake(grimpeur),
            PrendreBallon(intake),
            MonterIntake(grimpeur),
        )
        self.setName("Sequence Prendre")
