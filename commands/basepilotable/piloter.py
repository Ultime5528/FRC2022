import wpilib
from commands2 import CommandBase
from wpimath.filter import MedianFilter, LinearFilter
import properties
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

    def initialize(self) -> None:
        self.forward_filter = LinearFilter.movingAverage(int(properties.values.piloter_filter_size))
        self.turn_filter = LinearFilter.movingAverage(int(properties.values.piloter_filter_size))

    def execute(self):
        forward = interpoler(self.stick.getY(), properties.values.interpolation_courbure) * -1
        turn = interpoler(self.stick.getX(), properties.values.interpolation_courbure)

        self.base_pilotable.arcadeDrive(self.forward_filter.calculate(forward), self.turn_filter.calculate(turn))
