from commands.shooter.abstractshoot import AbstractShoot
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.shooter import Shooter


class InterpolatedShoot(AbstractShoot):
    def __init__(self, shooter: Shooter, intake: Intake, vision_targets: VisionTargets):
        super().__init__(shooter, intake)
        self.vision_targets = vision_targets

    def shoot(self) -> None:
        if self.vision_targets.hubFound:
            self.shooter.shoot_at_height(self.vision_targets.hubNormY)
        else:
            self.shooter.stop()
