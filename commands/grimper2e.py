import commands2

from commands.descendrecompletprimaire import DescendreCompletPrimaire
from subsystems.grimpeurprincipal import GrimpeurPrincipal


class Grimper2e(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_principal: GrimpeurPrincipal):
        super().__init__(
                DescendreCompletPrimaire(grimpeur_principal)
        )
        self.setName("Grimper2e")