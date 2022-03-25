import commands2
from subsystems.grimpeurprincipal import GrimpeurPrincipal


class DescendreCompletPrimaire(commands2.CommandBase):
    def __init__(self, grimpeur: GrimpeurPrincipal):
        super().__init__()
        self.grimpeur = grimpeur
        self.addRequirements(grimpeur)
        self.setName("DescendreCompletPrimaire")

    def execute(self) -> None:
        self.grimpeur.descendre()

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
        self.grimpeur.reset_encoder()
