import math

from commands2 import CommandBase
from subsystems.basepilotable import BasePilotable
from subsystems.visiontargets import VisionTargets
import properties


class ViserHub(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, visiontargets: VisionTargets):
        super().__init__()
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.visiontargets = visiontargets
        self.setName("Viser Hub")

        self.error = float("inf")

    def initialize(self) -> None:
        self.error = float("inf")

    def execute(self) -> None:
        if self.visiontargets.hubFound:
            self.error = self.visiontargets.hubNormX - properties.values.viser_hub_x_offset

            if self.error >= 0:
                self.base_pilotable.tankDrive(0, math.copysign(properties.values.viser_hub_speed, -1))
            else:
                self.base_pilotable.tankDrive(math.copysign(properties.values.viser_hub_speed, -1), 0)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return abs(self.error) <= properties.values.viser_hub_threshold
