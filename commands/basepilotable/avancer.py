import math


from subsystems.basepilotable import BasePilotable
from utils.properties import FloatProperty, to_callable
from utils.safecommandbase import SafeCommandBase


class Avancer(SafeCommandBase):
    def __init__(self, base_pilotable: BasePilotable, distance: FloatProperty, speed: FloatProperty) -> None:
        super().__init__()
        self.base_pilotable = base_pilotable
        self.get_distance = to_callable(distance)
        self.get_speed = to_callable(speed)
        self.addRequirements(base_pilotable)

    def initialize(self) -> None:
        self.base_pilotable.resetOdometry()

    def execute(self) -> None:
        self.base_pilotable.arcadeDrive(math.copysign(self.get_speed(), self.get_distance()), 0)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.base_pilotable.getAverageEncoderPosition()) >= abs(self.get_distance())
