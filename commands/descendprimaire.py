import commands2
from subsystems.grimpeur import Grimpeur


class DescendPrimaire(commands2.CommandBase):
    def __init__(self, bras_gauche: Grimpeur, switch_bas: Grimpeur):
        super().__init__()
        self.bras_gauche = bras_gauche
        self.switch = switch_bas

    def execute(self) -> None:
        self.grimpeur.descend()

    def isFinished(self) -> bool:
        return self.switch

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
