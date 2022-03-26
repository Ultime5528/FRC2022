import properties
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from utils.safecommandbase import SafeCommandBase
from utils.trapezoidalmotion import TrapezoidalMotion


class MonterCompletSecondaire(SafeCommandBase):
    def __init__(self, grimpeur: GrimpeurSecondaire):
        super().__init__()
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)
        self.motion = TrapezoidalMotion()

    def initialize(self) -> None:
        self.motion.update(
            start_position=self.grimpeur.getPosition(),
            end_position=properties.values.grimpeur_secondaire_hauteur_max,
            start_speed=properties.values.grimpeur_secondaire_start_speed,
            end_speed=properties.values.grimpeur_secondaire_end_speed,
            accel=properties.values.grimpeur_secondaire_accel,
        )

    def execute(self) -> None:
        self.motion.set_position(self.grimpeur.getPosition())
        self.grimpeur.set_moteur(self.motion.get_speed())

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchHaut()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
