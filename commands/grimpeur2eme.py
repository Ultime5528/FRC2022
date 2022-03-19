import commands2

from commands.retourswitch import RetourSwitch
from commands.descendresecondaire import DescendreSecondaire
from subsystems.grimpeur import Grimpeur


class Grimpeur2eme(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
            commands2.ParallelCommandGroup(
                RetourSwitch(grimpeur),
                DescendreSecondaire(grimpeur)
        ))
        self.setName("Grimper au 2eme")