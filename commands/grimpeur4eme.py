import commands2

from commands.bougersecondaire import BougerSecondaire
from commands.bougerprimaire import BougerPrimaire
from commands.descendrecompletprimaire import DescendreCompletPrimaire
from commands.descendrecompletsecondaire import DescendreCompletSecondaire
from subsystems.grimpeurprincipal import GrimpeurPrincipal
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class Grimpeur4eme(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_principal: GrimpeurPrincipal, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerPrimaire(grimpeur_principal, 5),
                DescendreCompletSecondaire(grimpeur_secondaire),
                DescendreCompletPrimaire(grimpeur_principal),
                BougerSecondaire(grimpeur_secondaire, 4),
                BougerPrimaire(grimpeur_principal, 10)
            ))
        self.setName("Grimper au 4eme")
