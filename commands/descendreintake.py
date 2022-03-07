from commands.montersecondaire import MonterSecondaire
from subsystems.grimpeur import Grimpeur


class DescendreIntake(MonterSecondaire):
    def __init__(self, grimpeur: Grimpeur):
        super(DescendreIntake, self).__init__(grimpeur)
        self.setName("Descendre Intake")
