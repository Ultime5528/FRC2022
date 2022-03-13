from typing import Callable
import commands2
from subsystems.grimpeur import Grimpeur


class MonterPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur, get_hauteur: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.get_hauteur = get_hauteur
        self.setName("Monter Primaire")
        self.addRequirements(self.grimpeur)

    def initialize(self) -> None:
        self.grimpeur.resetEncoder()

    def execute(self) -> None:
        self.grimpeur.monter()

    def isFinished(self) -> bool:
        return self.grimpeur.getPositionPrincipale() >= self.get_hauteur()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
