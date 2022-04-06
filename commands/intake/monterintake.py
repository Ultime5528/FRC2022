import commands2

from commands.grimpeur.bougersecondaire import BougerSecondaire
from commands.intake.arreterintake import ArreterIntake
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake


class MonterIntake(commands2.ParallelCommandGroup):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__(
            BougerSecondaire.to_intake_haut(grimpeur_secondaire),
        )
        self.setName(self.__class__.__name__)
