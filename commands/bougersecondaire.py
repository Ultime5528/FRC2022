from typing import Callable

import commands2
from subsystems.grimpeur import Grimpeur


class BougerSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur, position: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.position = position
        self.up = None
        self.setName("Bouger le Grimpeur Secondaire")
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        if self.grimpeur.getPositionSecondaire() >= self.position:
            self.grimpeur.descend_secondaire()
            self.up = False
        else:
            self.grimpeur.monter_secondaire()
            self.up = True

    def isFinished(self) -> bool:
        if self.grimpeur.getPositionSecondaire() > self.position and self.up == True:
            return True
        elif self.grimpeur.getPositionSecondaire() < self.position and self.up == False:
            return True
