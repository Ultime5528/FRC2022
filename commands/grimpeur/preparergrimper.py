import commands2

import properties
from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class PreparerGrimper(commands2.SequentialCommandGroup):
    def __init__(
            self,
            grimpeur_primaire: GrimpeurPrimaire,
            grimpeur_secondaire: GrimpeurSecondaire,
    ):
        super().__init__(
            commands2.ParallelCommandGroup(
                DescendreCompletPrimaire(grimpeur_primaire),
                commands2.SequentialCommandGroup(
                    DescendreCompletSecondaire(grimpeur_secondaire),
                    BougerSecondaire(
                        grimpeur_secondaire,
                        lambda: properties.values.grimpeur_secondaire_hauteur_alignement,
                    ),
                ),
            ),
            BougerPrimaire(
                grimpeur_primaire,
                lambda: properties.values.grimpeur_primaire_hauteur_clip,
            ),
            BougerSecondaire(
                grimpeur_secondaire,
                lambda: properties.values.grimpeur_secondaire_hauteur_alignement - 20,
            ),
            commands2.ParallelCommandGroup(
                DescendreCompletSecondaire(grimpeur_secondaire),
                BougerPrimaire(
                    grimpeur_primaire,
                    lambda: properties.values.grimpeur_primaire_hauteur_max,
                ),
            ),
        )
        self.setName(self.__class__.__name__)
