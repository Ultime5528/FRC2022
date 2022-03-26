import commands2

from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


# TODO Hauteurs lambda
class GrimperNiveau4(commands2.SequentialCommandGroup):
    def __init__(
        self,
        grimpeur_primaire: GrimpeurPrimaire,
        grimpeur_secondaire: GrimpeurSecondaire,
    ):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerPrimaire(grimpeur_primaire, 5),
                DescendreCompletSecondaire(grimpeur_secondaire),
                DescendreCompletPrimaire(grimpeur_primaire),
                BougerSecondaire(grimpeur_secondaire, 4),
                BougerPrimaire(grimpeur_primaire, 10),
            )
        )
        self.setName(self.__class__.__name__)
