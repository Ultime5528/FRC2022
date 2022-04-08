import commands2

from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire


class GrimperNiveau2(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_primaire: GrimpeurPrimaire):
        super().__init__(
            DescendreCompletPrimaire(grimpeur_primaire)
        )
        self.setName(self.__class__.__name__)
