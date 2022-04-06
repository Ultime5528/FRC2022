import commands2

from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


# TODO Hauteurs lambda
class GrimperNiveau4(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_primaire: GrimpeurPrimaire, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__(
            BougerSecondaire.to_max(grimpeur_secondaire),
            BougerPrimaire.to_max(grimpeur_primaire),
            BougerSecondaire.to_aligner_haut(grimpeur_secondaire),
            commands2.ParallelCommandGroup([
                BougerPrimaire.to_middle_lent(grimpeur_primaire),
                commands2.SequentialCommandGroup(
                    BougerSecondaire.to_next_level_lent(grimpeur_secondaire),
                    DescendreCompletSecondaire(grimpeur_secondaire),
                ),
            ]),
            DescendreCompletPrimaire(grimpeur_primaire),
            BougerSecondaire.to_next_level(grimpeur_secondaire),
            BougerPrimaire.to_max(grimpeur_primaire),
            BougerPrimaire.to_middle(grimpeur_primaire)
        )
        self.setName(self.__class__.__name__)
