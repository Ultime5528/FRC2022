import commands2

from subsystems.grimpeur import Grimpeur


class DescendreSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.setName("Descendre Secondaire")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        self.grimpeur.descend_secondaire()

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchBasSecondaire()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
