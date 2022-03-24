import commands2

from subsystems.grimpeursecondaire import GrimpeurSecondaire


class DescendreCompletSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__()
        self.setName("DescendreCompletSecondaire")
        self.grimpeur_secondaire = grimpeur_secondaire
        self.addRequirements(self.grimpeur_secondaire)

    def execute(self) -> None:
        self.grimpeur_secondaire.descendre()

    def isFinished(self) -> bool:
        return self.grimpeur_secondaire.getSwitchBas()

    def end(self, interrupted: bool) -> None:
        self.grimpeur_secondaire.stop()
        self.grimpeur_secondaire.reset_encoder()
