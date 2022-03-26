from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class MonterIntake(DescendreCompletSecondaire):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire):
        super(MonterIntake, self).__init__(grimpeur_secondaire)
        self.setName("Monter Intake")
        self.grimpeur = grimpeur_secondaire
        self.addRequirements(self.grimpeur)
