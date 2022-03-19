import commands2

from commands.bougersecondaire import BougerSecondaire
from commands.bougerprimaire import BougerPrimaire
from subsystems.grimpeur import Grimpeur


class Grimpeur3eme(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerSecondaire(grimpeur, 4),
                BougerPrimaire(grimpeur, 10),
                BougerSecondaire(grimpeur, 5),
                BougerPrimaire(grimpeur, 8)
        ))
        self.setName("Grimper au 3eme")