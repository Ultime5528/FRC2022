from commands.descendresecondaire import DescendreSecondaire
from subsystems.grimpeur import Grimpeur


class DescendreIntake(DescendreSecondaire):
    def __init__(self, grimpeur: Grimpeur):
        super(DescendreIntake, self).__init__(grimpeur)
        self.setName("Descendre Intake")
