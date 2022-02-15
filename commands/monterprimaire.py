import commands2
from subsystems.grimpeur import Grimpeur


class MonterPrimaire(commands2.CommandBase):
    def __init__(self, bras_gauche: Grimpeur, switch_haut: Grimpeur):
        super().__init__()
        self.bras_gauche = bras_gauche
        self.switch = switch_haut

    def execute(self) -> None:
        self.grimpeur.monter()

    def isFinished(self,) -> bool:
        return self.switch

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
