from commands2 import CommandBase
from subsystems.basepilotable import BasePilotable
from subsystems.visionhub import VisionHub
import properties


class ViserHub(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, visionhub: VisionHub):
        super().__init__()
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.visionhub = visionhub
        self.setName("Viser hub")

    def initialize(self) -> None:
        self.error = float("inf")

    def execute(self) -> None:
        self.error = self.visionhub.normX - properties.viser_hub_x_offset
        if self.error >= 0:
            self.base_pilotable.rightDrive(-properties.viser_hub_speed)
        else:
            self.base_pilotable.leftDrive(-properties.viser_hub_speed)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.error) <= properties.viser_hub_threshold
