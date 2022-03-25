import commands2

import properties
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from utils.trapezoidalmotion import TrapezoidalMotion


class DescendreCompletSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__()
        self.setName("DescendreCompletSecondaire")
        self.grimpeur_secondaire = grimpeur_secondaire
        self.addRequirements(self.grimpeur_secondaire)
        self.motion = TrapezoidalMotion(end_position=0)

    def initialize(self) -> None:
        self.motion.update(
            start_position=self.grimpeur_secondaire.getPosition(),
            start_speed=properties.values.grimpeur_secondaire_start_speed,
            end_speed=properties.values.grimpeur_secondaire_end_speed,
            accel=properties.values.grimpeur_secondaire_accel
        )

    def execute(self) -> None:
        self.motion.set_position(self.grimpeur_secondaire.getPosition())
        self.grimpeur_secondaire.set_moteur(self.motion.get_speed())

    def isFinished(self) -> bool:
        return self.grimpeur_secondaire.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur_secondaire.stop()
        if not interrupted:
            self.grimpeur_secondaire.reset_encoder()
