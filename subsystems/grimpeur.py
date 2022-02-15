import rev
import wpilib
import commands2
import ports
from wpilib import DigitalInput

import properties


class Grimpeur(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.switch_bas = DigitalInput(ports.digital_switch_grimpeur_bas)
        self.switch_haut = DigitalInput(ports.digital_switch_grimpeur_haut)
        # Motors
        self.bras_droit = rev.CANSparkMax(ports.grimpeur_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self.bras_gauche = rev.CANSparkMax(ports.grimpeur_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self.bras_droit.follow(self.bras_gauche, invert=True)

    def monter(self):
        self.bras_gauche.set(properties.vitesse_grimpeur_monter)

    def descend(self):
        self.bras_gauche.set(properties.vitesse_grimpeur_descend)

    def stop(self):
        self.bras_gauche.set(0)
        self.bras_gauche_sec.set(0)
