import commands2
from subsystems.grimpeur import Grimpeur


class DescendrePrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.grimpeur = grimpeur
        self.setName("Descendre Primaire")

    def execute(self) -> None:
        self.grimpeur.descend()

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
