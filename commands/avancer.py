import commands2
from subsystems.basepilotable import BasePilotable
import math


class Avancer(commands2.CommandBase):
    def __init__(self, base_pilotable: BasePilotable, distance: float, speed: float) -> None:
        super().__init__()
        self.base_pilotable = base_pilotable
        self.distance = distance
        self.speed = speed
        self.addRequirements(base_pilotable)
        self.setName('Avancer')

    def initialize(self) -> None:
        self.base_pilotable.resetOdometry()

    def execute(self) -> None:
        self.base_pilotable.arcadeDrive(math.copysign(self.speed, self.distance), 0)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.base_pilotable.getAverageEncoderPosition()) >= abs(self.distance)
