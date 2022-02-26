import commands2

from subsystems.grimpeur import Grimpeur


class DescendreSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: Grimpeur):
        super().__init__()
        self.setName("descendre secondaire")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        self.grimpeur.descend_secondaire()

    def isFinished(self) -> bool:
        return self.grimpeur.switch_bas_secondaire.get()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
