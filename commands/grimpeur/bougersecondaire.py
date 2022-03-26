from typing import Callable
import commands2
import wpilib
import properties

from subsystems.grimpeursecondaire import GrimpeurSecondaire
from utils.properties import FloatProperty, to_callable
from utils.trapezoidalmotion import TrapezoidalMotion


class BougerSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: GrimpeurSecondaire, position: FloatProperty):
        super().__init__()
        self.setName("BougerSecondaire")
        self.grimpeur = grimpeur
        self.get_position = to_callable(position)
        self.addRequirements(self.grimpeur)
        self.motion = TrapezoidalMotion()

    def initialize(self) -> None:
        self.motion.update(
            start_position=self.grimpeur.getPosition(),
            end_position=self.get_position(),
            start_speed=properties.values.grimpeur_secondaire_start_speed,
            end_speed=properties.values.grimpeur_secondaire_end_speed,
            accel=properties.values.grimpeur_secondaire_accel,
        )

    def execute(self) -> None:
        self.motion.set_position(self.grimpeur.getPosition())
        self.grimpeur.set_moteur(self.motion.get_speed())

    def isFinished(self) -> bool:
        return self.motion.is_finished()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
