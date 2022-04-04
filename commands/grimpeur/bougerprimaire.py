from typing import Optional

import properties
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from utils.properties import FloatProperty, to_callable
from utils.safecommandbase import SafeCommandBase
from utils.trapezoidalmotion import TrapezoidalMotion


class BougerPrimaire(SafeCommandBase):
    @classmethod
    def to_clip(cls, grimpeur: GrimpeurPrimaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_primaire_hauteur_clip)
        cmd.setName(cmd.getName() + " clip")
        return cmd

    @classmethod
    def to_min(cls, grimpeur: GrimpeurPrimaire):
        cmd = cls(grimpeur, 5)  # presque zéro
        cmd.setName(cmd.getName() + " min")
        return cmd

    @classmethod
    def to_max(cls, grimpeur: GrimpeurPrimaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_primaire_hauteur_max)
        cmd.setName(cmd.getName() + " max")
        return cmd

    @classmethod
    def to_middle(cls, grimpeur: GrimpeurPrimaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_primaire_hauteur_max/2)
        cmd.setName(cmd.getName() + " middle")
        return cmd

    @classmethod
    def to_middle_lent(cls, grimpeur: GrimpeurPrimaire):
        cmd = cls(
            grimpeur,
            lambda: properties.values.grimpeur_primaire_hauteur_max / 2,
            lambda: properties.values.grimpeur_primaire_vitesse_descendre_slow
        )
        cmd.setName(cmd.getName() + " middle lent")
        return cmd

    def __init__(self, grimpeur: GrimpeurPrimaire, hauteur: FloatProperty, speed: Optional[FloatProperty] = None):
        super().__init__()
        if not speed:
            speed = lambda: properties.values.grimpeur_primaire_end_speed
        self.get_speed = to_callable(speed)
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
        self.get_hauteur = to_callable(hauteur)
        self.motion = TrapezoidalMotion()

    def initialize(self) -> None:
        self.motion.update(
            start_position=self.grimpeur.getPosition(),
            end_position=self.get_hauteur(),
            start_speed=properties.values.grimpeur_primaire_start_speed,
            end_speed=self.get_speed(),
            accel=properties.values.grimpeur_primaire_accel
        )

    def execute(self) -> None:
        self.motion.set_position(self.grimpeur.getPosition())
        self.grimpeur.set_moteur(self.motion.get_speed())

    def isFinished(self) -> bool:
        return self.motion.is_finished()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
