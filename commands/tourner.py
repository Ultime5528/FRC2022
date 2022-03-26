import math
from commands2 import CommandBase
from subsystems.basepilotable import BasePilotable


class Tourner(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, angle: float, speed: float):
        super().__init__()
        self.angle = angle
        self.speed = speed
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Tourner")

    def initialize(self) -> None:
        self.base_pilotable.resetOdometry()

    def execute(self):
        # self.base_pilotable.arcadeDrive(-1, 1)
        self.base_pilotable.arcadeDrive(0, math.copysign(self.speed, self.angle))

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.base_pilotable.getAngle()) >= abs(self.angle)
