from commands.montercompletsecondaire import MonterCompletSecondaire
from subsystems.grimpeur import Grimpeur


class DescendreIntake(MonterCompletSecondaire):
    def __init__(self, grimpeur: Grimpeur):
        super(DescendreIntake, self).__init__(grimpeur)
        self.setName("Descendre Intake")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
