from typing import Callable
import commands2
from subsystems.grimpeur import Grimpeur


class BougerSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur, hauteur: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.position = hauteur
        self.up = None
        self.setName("Bouger le Grimpeur Secondaire")
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        if self.grimpeur.getPositionSecondaire() >= self.position and self.up is not True:
            self.grimpeur.descend_secondaire()
            self.up = False
        elif self.up is not True:
            self.grimpeur.monter_secondaire()
            self.up = True

    def isFinished(self) -> bool:
        if self.grimpeur.getPositionSecondaire() > self.position and self.up:
            return True
        elif self.grimpeur.getPositionSecondaire() < self.position and not self.up:
            return True
        else:
            return False

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop_secondaire()
