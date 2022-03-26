import commands2

from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


# TODO Hauteurs lambda
class GrimperNiveau3(commands2.SequentialCommandGroup):
    def __init__(
        self,
        grimpeur_primaire: GrimpeurPrimaire,
        grimpeur_secondaire: GrimpeurSecondaire,
    ):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerSecondaire(grimpeur_secondaire, 4),
                BougerPrimaire(grimpeur_primaire, 10),
                BougerSecondaire(grimpeur_secondaire, 5),
                BougerPrimaire(grimpeur_primaire, 8),
            )
        )
        self.setName(self.__class__.__name__)
