from utils.safecommandbase import SafeCommandBase
import wpilib
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets


class PreparerInterpolated(SafeCommandBase):
    def __init__(self, shooter: Shooter, vision_targets: VisionTargets):
        super(self).__init__()
        self.shooter = shooter
        self.vision_targets = vision_targets

    def execute(self) -> None:
        self.shooter.shoot_at_height(self.vision_targets.hubNormY)

    def isFinished(self) -> bool:
        return False
