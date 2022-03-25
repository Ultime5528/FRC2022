import commands2

import properties
from subsystems.grimpeurprincipal import GrimpeurPrincipal
from utils.trapezoidalmotion import TrapezoidalMotion


class DescendreCompletPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: GrimpeurPrincipal):
        super().__init__()
        self.grimpeur = grimpeur
        self.addRequirements(grimpeur)
        self.setName("DescendreCompletPrimaire")
        self.motion = TrapezoidalMotion(end_position=0)

    def initialize(self) -> None:
        self.motion.update(
            start_position=self.grimpeur.getPosition(),
            start_speed=properties.values.grimpeur_principal_start_speed,
            end_speed=properties.values.grimpeur_principal_end_speed,
            accel=properties.values.grimpeur_principal_accel
        )

    def execute(self) -> None:
        self.motion.set_position(self.grimpeur.getPosition())
        self.grimpeur.set_moteur(self.motion.get_speed())

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
        if not interrupted:
            self.grimpeur.reset_encoder()
