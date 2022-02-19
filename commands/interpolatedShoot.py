import commands2
from subsystems.visiontargets import VisionTargets
from utils.linearInterpolator import LinearInterpolator
from subsystems.shooter import Shooter
from wpilib import Joystick


class InterpolatedShoot(commands2.CommandBase):
    def __init__(self, shooter: Shooter, vision_targets: VisionTargets, stick: Joystick):
        super().__init__()
        self.shooter = shooter
        self.vision_targets = vision_targets

    def execute(self) -> None:
        self.shooter.shoot_at_height(self.vision_targets.normY)

    def end(self, interrupted: bool) -> None:
        self.shooter.disable()
