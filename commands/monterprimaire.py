import commands2
from subsystems.grimpeur import Grimpeur


class MonterPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.grimpeur = grimpeur
        self.setName("grimper")
    def execute(self) -> None:
        self.grimpeur.monter()

    def isFinished(self) -> bool:
        return self.grimpeur.switch_haut.get()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()