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
        if self.vision_targets.hubFound:
            self.shooter.shoot_at_height(self.vision_targets.hubNormY)
        else:
            self.shooter.stop()

    def isFinished(self) -> bool:
        return False
