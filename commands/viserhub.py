from commands2 import CommandBase
from subsystems.basepilotable import BasePilotable
from subsystems.visionhub import VisionHub
from constants import Properties


class ViserHub(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, visionhub: VisionHub, targetX):
        super().__init__()
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.visionhub = visionhub
        self.setName("Viser hub")
        self.targetX = targetX
        self.speed = Properties.viser_speed
        self.offset = Properties.viser_offset

    def initialize(self) -> None:
        self.error = float("inf")

    def execute(self) -> None:
        self.error = self.visionhub.normX - self.targetX
        print(self.error)
        if abs(self.error) > self.offset:
            if self.visionhub.normX >= 0:
                self.base_pilotable.rightDrive(-self.speed)
            else:
                self.base_pilotable.leftDrive(-self.speed)


    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.error) <= self.offset
