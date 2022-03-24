import commands2

from commands.bougersecondaire import BougerSecondaire
from commands.bougerprimaire import BougerPrimaire
from subsystems.grimpeurprincipal import GrimpeurPrincipal
from subsystems.grimpeursecondaire import GrimpeurSecondaire


class Grimpeur3eme(commands2.SequentialCommandGroup):
    def __init__(self, grimpeur_primaire: GrimpeurPrincipal, grimpeur_secondaire: GrimpeurSecondaire):
        super().__init__(
            commands2.SequentialCommandGroup(
                BougerSecondaire(grimpeur_secondaire, 4),
                BougerPrimaire(grimpeur_primaire, 10),
                BougerSecondaire(grimpeur_secondaire, 5),
                BougerPrimaire(grimpeur_primaire, 8)
        ))
        self.setName("Grimper au 3eme")