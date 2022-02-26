from commands2 import CommandBase
import wpilib
from subsystems.basepilotable import BasePilotable


class Piloter(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, stick: wpilib.Joystick):
        super().__init__()

        self.stick = stick
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Piloter")

    def interpoler(self, valeur: float, courbure=1.0, deadzoneY=0.1, deadzoneX=0.1):

        if valeur >= deadzoneX:
            return deadzoneY + (1 - deadzoneY) * (courbure * valeur * valeur * valeur + (1 - courbure) * valeur);
        elif valeur <= -deadzoneX:
            return -deadzoneY + (1 - deadzoneY) * (courbure * valeur * valeur * valeur + (1 - courbure) * valeur);
        else:
            return 0.0  # interpolate(deadzoneX) / deadzoneX * valeur;

    def execute(self):
        self.base_pilotable.arcadeDrive(self.interpoler(self.stick.getY()) * -1, self.interpoler(self.stick.getX()))
    