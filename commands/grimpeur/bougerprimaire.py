from typing import Callable

import properties
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from utils.safecommandbase import SafeCommandBase
from utils.trapezoidalmotion import TrapezoidalMotion


class BougerPrimaire(SafeCommandBase):
    def __init__(self, grimpeur: GrimpeurPrimaire, get_hauteur: Callable[[], float]):
        super().__init__()
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
        self.get_hauteur = get_hauteur
        self.motion = TrapezoidalMotion()

    def initialize(self) -> None:
        self.motion.update(
            start_position=self.grimpeur.getPosition(),
            end_position=self.get_hauteur(),
            start_speed=properties.values.grimpeur_primaire_start_speed,
            end_speed=properties.values.grimpeur_primaire_end_speed,
            accel=properties.values.grimpeur_primaire_accel
        )

    def execute(self) -> None:
        self.motion.set_position(self.grimpeur.getPosition())
        self.grimpeur.set_moteur(self.motion.get_speed())

    def isFinished(self) -> bool:
        return self.motion.is_finished()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
