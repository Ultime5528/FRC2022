import commands2

import properties
from commands.bougerprimaire import BougerPrimaire
from commands.bougersecondaire import BougerSecondaire
from commands.descendrecompletprimaire import DescendreCompletPrimaire
from commands.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeur import Grimpeur


class PreparerGrimper(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
            commands2.ParallelCommandGroup(
                DescendreCompletPrimaire(grimpeur),
                commands2.SequentialCommandGroup(
                    DescendreCompletSecondaire(grimpeur),
                    BougerSecondaire(grimpeur, lambda: properties.values.grimpeur_distance_alignement)
                )
            ),
            BougerPrimaire(grimpeur, lambda: properties.values.grimpeur_primaire_hauteur_clip),
            DescendreCompletSecondaire(grimpeur),
            BougerPrimaire(grimpeur, lambda: properties.values.grimpeur_primaire_hauteur_max)
        )
        self.setName("PreparerGrimper")
