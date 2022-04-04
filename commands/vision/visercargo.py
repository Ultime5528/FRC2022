import math
import properties
from subsystems.basepilotable import BasePilotable
from subsystems.visiontargets import VisionTargets
from utils.safecommandbase import SafeCommandBase


class ViserCargo(SafeCommandBase):
    def __init__(self, base_pilotable: BasePilotable, vision_targets: VisionTargets):
        super().__init__()
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.vision_targets = vision_targets
        self.x_stop = False
        self.y_stop = False
        self._reset()

    def _reset(self):
        self.x_stop = False
        self.y_stop = False

    def initialize(self) -> None:
        self._reset()

    def execute(self) -> None:
        nearest = self.vision_targets.nearestCargo

        if nearest:
            x_error = nearest.nx - properties.values.viser_cargo_x_offset
            y_error = nearest.ny - properties.values.viser_cargo_y_offset

            self.x_stop = abs(x_error) <= properties.values.viser_cargo_x_threshold
            self.y_stop = abs(y_error) <= properties.values.viser_cargo_y_threshold

            x_speed = min(properties.values.viser_cargo_turn_speed * abs(x_error), 0.3)
            x_speed = math.copysign(x_speed, x_error)

            if self.y_stop:
                y_speed = 0
            else:
                y_speed = math.copysign(
                    properties.values.viser_cargo_forward_speed, y_error
                )

            self.base_pilotable.arcadeDrive(y_speed, x_speed)
        else:
            self.base_pilotable.arcadeDrive(0, 0)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return self.x_stop and self.y_stop
