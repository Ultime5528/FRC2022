from typing import Callable
import commands2
from subsystems.grimpeurprincipal import GrimpeurPrincipal


class BougerPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: GrimpeurPrincipal, get_hauteur: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.get_hauteur = get_hauteur
        self.up = None
        self.setName("BougerPrimaire")
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        if self.grimpeur.getPosition() >= self.get_hauteur() and self.up is not True:
            self.grimpeur.descendre()
            self.up = False
        elif self.up is not False:
            self.grimpeur.monter()
            self.up = True

    def isFinished(self) -> bool:
        if self.grimpeur.getPosition() > self.get_hauteur() and self.up:
            return True
        elif self.grimpeur.getPosition() < self.get_hauteur() and not self.up:
            return True
        else:
            return False

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
