from commands2 import CommandBase
from subsystems.basepilotable import BasePilotable
from subsystems.hub_sub import Hub_sub

class VisionHub(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, hub_sub: Hub_sub, targetX ):
        super().__init__()
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.hub_sub = hub_sub
        self.addRequirements(hub_sub)
        self.setName("Viser hub")
        self.targetX = targetX
        self.speed = 0.25
        self.offset = 0.05


    def initialize(self) -> None:
        self.error = float("inf")

    def execute(self) -> None:
        self.error = self.hub_sub.normX - self.targetX + self.offset
        if self.error >= self.offset:
            self.base_pilotable.rightDrive(self.speed)
        elif self.error.error <= -self.offset:
            self.base_pilotable.leftDrive(self.speed)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.error) <= self.offset
