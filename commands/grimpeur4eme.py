import commands2

from commands.bougersecondaire import BougerSecondaire
from commands.bougerprimaire import BougerPrimaire
from commands.descendresecondaire import DescendreSecondaire
from commands.retourswitch import RetourSwitch
from subsystems.grimpeur import Grimpeur


class Grimpeur4eme(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerPrimaire(grimpeur, 5),
                DescendreSecondaire(grimpeur),
                RetourSwitch(grimpeur),
                BougerSecondaire(grimpeur, 4),
                BougerPrimaire(grimpeur, 10)
            ))
        self.setName("Grimper au 4eme")
