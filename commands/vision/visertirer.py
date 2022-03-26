import commands2
from wpilib import Joystick

from commands.basepilotable.piloter import Piloter
from commands.shooter.dashboardshoot import DashboardShoot
from commands.vision.viserhub import ViserHub
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets


class ViserTirer(commands2.SequentialCommandGroup):
    def __init__(
        self, basepilotable: BasePilotable, stick: Joystick, shooter: Shooter, intake: Intake, vision: VisionTargets
    ):
        super().__init__(
            ViserHub(basepilotable, vision),
            commands2.ParallelDeadlineGroup(DashboardShoot(shooter, intake), Piloter(basepilotable, stick)),
        )
