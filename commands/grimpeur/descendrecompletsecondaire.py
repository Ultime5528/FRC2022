from subsystems.grimpeursecondaire import GrimpeurSecondaire
from utils.safecommandbase import SafeCommandBase


class DescendreCompletSecondaire(SafeCommandBase):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__()
        self.grimpeur_secondaire = grimpeur_secondaire
        self.addRequirements(self.grimpeur_secondaire)

    def execute(self) -> None:
        self.grimpeur_secondaire.descendre()

    def isFinished(self) -> bool:
        return self.grimpeur_secondaire.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur_secondaire.stop()
        if not interrupted:
            self.grimpeur_secondaire.reset_encoder()
