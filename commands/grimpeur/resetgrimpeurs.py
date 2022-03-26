import commands2

from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class ResetGrimpeurs(commands2.ParallelCommandGroup):
    def __init__(self, grimpeur_primaire: GrimpeurPrimaire, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__(
            DescendreCompletPrimaire(grimpeur_primaire),
            DescendreCompletSecondaire(grimpeur_secondaire)
        )
        self.setName(self.__class__.__name__)
