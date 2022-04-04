import commands2
from wpilib import Joystick

from commands.basepilotable.piloter import Piloter
from commands.shooter.interpolatedshoot import InterpolatedShoot
from commands.vision.viserhub import ViserHub
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets
from commands.shooter.preparerinterpolated import PreparerInterpolated


class ViserTirer(commands2.SequentialCommandGroup):
    def __init__(
            self, basepilotable: BasePilotable, stick: Joystick, shooter: Shooter, intake: Intake, vision_targets: VisionTargets
    ):
        super().__init__(
            commands2.ParallelDeadlineGroup(
                ViserHub(basepilotable, vision_targets),
                PreparerInterpolated(shooter, vision_targets)
            ),
            commands2.ParallelDeadlineGroup(
                InterpolatedShoot(shooter, intake, vision_targets),
                Piloter(basepilotable, stick)
            ),
        )
        self.setName(self.__class__.__name__)
