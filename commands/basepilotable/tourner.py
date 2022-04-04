import math


from subsystems.basepilotable import BasePilotable
from utils.safecommandbase import SafeCommandBase


class Tourner(SafeCommandBase):
    def __init__(self, base_pilotable: BasePilotable, angle: float, speed: float):
        super().__init__()
        self.angle = angle
        self.speed = speed
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)

    def initialize(self) -> None:
        self.base_pilotable.resetOdometry()

    def execute(self):
        # self.base_pilotable.arcadeDrive(-1, 1)
        self.base_pilotable.arcadeDrive(0, math.copysign(self.speed, self.angle))

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.base_pilotable.getAngle()) >= abs(self.angle)
