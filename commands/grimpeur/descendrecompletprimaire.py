from subsystems.grimpeurprimaire import GrimpeurPrimaire
from utils.safecommandbase import SafeCommandBase


class DescendreCompletPrimaire(SafeCommandBase):
    def __init__(self, grimpeur: GrimpeurPrimaire):
        super().__init__()
        self.grimpeur = grimpeur
        self.addRequirements(grimpeur)

    def execute(self) -> None:
        self.grimpeur.descendre()

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
        if not interrupted:
            self.grimpeur.reset_encoder()
