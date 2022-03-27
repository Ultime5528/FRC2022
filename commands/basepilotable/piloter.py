import wpilib
from commands2 import CommandBase

from subsystems.basepilotable import BasePilotable


def interpoler(valeur: float, courbure=0.6, deadzoneY=0.05, deadzoneX=0.05):
    if valeur >= deadzoneX:
        return deadzoneY + (1 - deadzoneY) * (courbure * valeur * valeur * valeur + (1 - courbure) * valeur)
    elif valeur <= -deadzoneX:
        return -deadzoneY + (1 - deadzoneY) * (courbure * valeur * valeur * valeur + (1 - courbure) * valeur)
    else:
        return 0.0  # interpolate(deadzoneX) / deadzoneX * valeur;


class Piloter(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, stick: wpilib.Joystick):
        super().__init__()

        self.stick = stick
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Piloter")

    def execute(self):
        self.base_pilotable.arcadeDrive(interpoler(self.stick.getY()) * -1, interpoler(self.stick.getX()))