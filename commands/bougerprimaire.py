from typing import Callable
import commands2
from subsystems.grimpeur import Grimpeur


class BougerPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur, get_hauteur: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.get_hauteur = get_hauteur
        self.setName("Monter Primaire")

    def execute(self) -> None:
        self.grimpeur.getPositionPrincipale()
        self.grimpeur.monter()

    def isFinished(self) -> bool:
        if self.grimpeur.getPositionPrincipale() > self.position and self.up == True:
            return True
        elif self.grimpeur.getPositionPrincipale() < self.position and self.up == False:
            return True

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
