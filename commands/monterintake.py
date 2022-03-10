from commands.descendresecondaire import DescendreSecondaire
from subsystems.grimpeur import Grimpeur


class MonterIntake(DescendreSecondaire):
    def __init__(self, grimpeur: Grimpeur):
        super(MonterIntake, self).__init__(grimpeur)
        self.setName("Monter Intake")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
