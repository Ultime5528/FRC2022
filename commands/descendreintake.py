from commands.grimpeur.montercompletsecondaire import MonterCompletSecondaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class DescendreIntake(MonterCompletSecondaire):
    def __init__(self, grimpeur: GrimpeurSecondaire):
        super().__init__(grimpeur)
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
