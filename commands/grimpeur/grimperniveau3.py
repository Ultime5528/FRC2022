import commands2

from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


# TODO Hauteurs lambda
class GrimperNiveau3(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_primaire: GrimpeurPrimaire, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__(
            BougerSecondaire.to_next_level(grimpeur_secondaire),
            BougerPrimaire.to_max(grimpeur_primaire),
            BougerPrimaire.to_middle(grimpeur_primaire)
        )
        self.setName(self.__class__.__name__)
