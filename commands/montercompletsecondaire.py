import commands2

from subsystems.grimpeursecondaire import GrimpeurSecondaire


class MonterCompletSecondaire(commands2.CommandBase):
    def __init__(self, grimpeur: GrimpeurSecondaire):
        super().__init__()
        self.setName("MonterCompletSecondaire")
        self.grimpeur = grimpeur
        self.addRequirements(self.grimpeur)

    def execute(self) -> None:
        self.grimpeur.monter()

    def isFinished(self) -> bool:
        return self.grimpeur.getSwitchHaut()

    def end(self, interrupted: bool) -> None:
        self.grimpeur.stop()
