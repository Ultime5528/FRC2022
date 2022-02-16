import math

from commands2 import CommandBase
from subsystems.basepilotable import BasePilotable
from subsystems.visiontargets import VisionTargets
import properties


class ViserCargo(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, visiontargets: VisionTargets):
        super().__init__()
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.visiontargets = visiontargets
        self.setName("Viser cargo")

    def initialize(self) -> None:
        self.x_stop = False
        self.y_stop = False

    def execute(self) -> None:
        x_error = self.visiontargets.cargoNormX - properties.viser_cargo_x_offset
        y_error = self.visiontargets.cargoNormY - properties.viser_cargo_y_offset

        self.x_stop = abs(x_error) <= properties.viser_cargo_x_threshold
        self.y_stop = abs(y_error) <= properties.viser_cargo_y_threshold

        if self.x_stop:
            x_speed = 0
        else:
            x_speed = math.copysign(properties.viser_cargo_turn_speed, x_error)

        if self.y_stop:
            y_speed = 0
        else:
            y_speed = math.copysign(properties.viser_cargo_forward_speed, y_error)

        self.base_pilotable.arcadeDrive(y_speed, x_speed)

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return self.x_stop and self.y_stop
