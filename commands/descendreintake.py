from commands.montercompletsecondaire import MonterCompletSecondaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class DescendreIntake(MonterCompletSecondaire):
    def __init__(self, grimpeur: GrimpeurSecondaire):
        super(DescendreIntake, self).__init__(grimpeur)
        self.setName("Descendre Intake")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
