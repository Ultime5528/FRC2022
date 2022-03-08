import commands2
from subsystems.grimpeur import Grimpeur


class MonterSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.setName("Monter Secondaire")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        self.grimpeur.monter_secondaire()

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchHautSecondaire()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
