import commands2

from commands.bougersecondaire import BougerSecondaire
from commands.bougerprimaire import BougerPrimaire
from commands.descendrecompletprimaire import DescendreCompletPrimaire
from commands.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeur import Grimpeur


class Grimpeur4eme(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerPrimaire(grimpeur, 5),
                DescendreCompletSecondaire(grimpeur),
                DescendreCompletPrimaire(grimpeur),
                BougerSecondaire(grimpeur, 4),
                BougerPrimaire(grimpeur, 10)
            ))
        self.setName("Grimper au 4eme")
