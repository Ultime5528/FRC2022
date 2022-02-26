import commands2
from subsystems.grimpeur import Grimpeur


class DescendPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.grimpeur = grimpeur
        self.setName("descendre")
    def execute(self) -> None:
        self.grimpeur.descend()

    def isFinished(self) -> bool:
        return self.grimpeur.switch_bas.get()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()