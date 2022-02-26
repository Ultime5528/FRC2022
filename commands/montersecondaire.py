import commands2
from subsystems.grimpeur import Grimpeur


class Montersecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.setName("monter secondaire")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        self.grimpeur.monter_secondaire()

    def isFinished(self) -> bool:
        return self.grimpeur._switch_haut_secondaire.get()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
