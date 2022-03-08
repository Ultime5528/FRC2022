import commands2

import properties
from subsystems.grimpeur import Grimpeur


class MonterPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.grimpeur = grimpeur
        self.setName("Monter Primaire")

    def initialize(self) -> None:
        self.grimpeur.resetEncoder()

    def execute(self) -> None:
        self.grimpeur.monter()

    def isFinished(self) -> bool:
        if self.grimpeur.getPositionPrincipale() >= properties.values.grimpeur_enconder_monter:
            return True

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
