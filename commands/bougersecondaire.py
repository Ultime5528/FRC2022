from typing import Callable
import commands2
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class BougerSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: GrimpeurSecondaire, get_position: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.get_position = get_position
        self.up = None
        self.setName("Bouger Le Grimpeur Secondaire")
        self.addRequirements(self.grimpeur)

    def initialize(self) -> None:
        self.up = None

    def execute(self) -> None:
        if self.grimpeur.getPosition() >= self.get_position() and self.up is not True:
            self.grimpeur.descendre()
            self.up = False
        elif self.up is not True:
            self.grimpeur.monter()
            self.up = True

    def isFinished(self) -> bool:
        if self.grimpeur.getPosition() > self.get_position() and self.up:
            return True
        elif self.grimpeur.getPosition() < self.get_position() and not self.up:
            return True
        else:
            return False

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
