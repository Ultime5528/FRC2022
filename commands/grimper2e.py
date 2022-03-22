import commands2

from commands.descendrecompletprimaire import DescendreCompletPrimaire
from subsystems.grimpeur import Grimpeur


class Grimper2e(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
                DescendreCompletPrimaire(grimpeur)
        )
        self.setName("Grimper2e")