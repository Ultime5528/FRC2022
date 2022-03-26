import commands2

from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from subsystems.grimpeurprimaire import GrimpeurPrimaire


class GrimperNiveau2(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_principal: GrimpeurPrimaire):
        super().__init__(DescendreCompletPrimaire(grimpeur_principal))
        self.setName(self.__class__.__name__)
