import properties
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from utils.properties import FloatProperty, to_callable
from utils.safecommandbase import SafeCommandBase
from utils.trapezoidalmotion import TrapezoidalMotion


class BougerSecondaire(SafeCommandBase):
    @classmethod
    def to_next_level(cls, grimpeur: GrimpeurSecondaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_primaire_hauteur_level_3)
        cmd.setName(cmd.getName() + " level 3")
        return cmd

    @classmethod
    def to_max(cls, grimpeur: GrimpeurSecondaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_secondaire_hauteur_max)
        cmd.setName(cmd.getName() + " max")
        return cmd

    @classmethod
    def to_aligner_bas(cls, grimpeur: GrimpeurSecondaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_secondaire_hauteur_alignement_bas)
        cmd.setName(cmd.getName() + " aligner bas")
        return cmd

    @classmethod
    def to_aligner_haut(cls, grimpeur: GrimpeurSecondaire):
        cmd = cls(grimpeur, lambda: properties.values.grimpeur_secondaire_hauteur_alignement_haut)
        cmd.setName(cmd.getName() + " aligner haut")
        return cmd

    def __init__(self, grimpeur: GrimpeurSecondaire, position: FloatProperty):
        super().__init__()
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
