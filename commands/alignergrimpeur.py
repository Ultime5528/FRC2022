import commands2

from commands.montersecondaire import MonterSecondaire
from subsystems.grimpeur import Grimpeur
import properties

__all__ = ["AlignerGrimpeur"]


class _AlignerGrimpeur(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.grimpeur = grimpeur
        self.setName("_Aligner Grimpeur")
        self.addRequirements(self.grimpeur)

    def initialize(self) -> None:
        self.positionInitial = self.grimpeur.getPositionSecondaire()

    def execute(self) -> None:
        self.grimpeur.descend_secondaire()

    def isFinished(self) -> bool:
        return (self.positionInitial - self.grimpeur.getPositionSecondaire()) >= \
               properties.values.distance_alignement_grimpeur


class AlignerGrimpeur(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__(
            MonterSecondaire(grimpeur),
            _AlignerGrimpeur(grimpeur)
        )
        self.setName("Aligner Grimpeur")