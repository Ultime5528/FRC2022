import commands2
from wpilib import Joystick
from wpimath.geometry import Pose2d, Rotation2d

from commands.basepilotable.avancer import Avancer
from commands.basepilotable.suivretrajectoire import SuivreTrajectoire
from commands.intake.descendreintake import DescendreIntake
from commands.intake.prendreballon import PrendreBallon
from commands.vision.visertirer import ViserTirer
from subsystems.basepilotable import BasePilotable
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets


class Auto4Ballons(commands2.SequentialCommandGroup):
    def __init__(
            self,
            base_pilotable: BasePilotable,
            grimpeur: GrimpeurSecondaire,
            stick: Joystick,
            shooter: Shooter,
            intake: Intake,
            vision: VisionTargets
    ):
        super().__init__(
            commands2.ParallelCommandGroup(
                Avancer(base_pilotable, 3, 0.3),
                commands2.SequentialCommandGroup(
                    DescendreIntake(grimpeur),
                    PrendreBallon(intake)
                )
            ),
            ViserTirer(base_pilotable, stick, shooter, intake, vision),
            commands2.ParallelCommandGroup(
                SuivreTrajectoire(base_pilotable,
                              [Pose2d(3, 1, Rotation2d.fromDegrees(0))],
                              0.2, addRobotPose=True),
                PrendreBallon(intake),
            ),
            commands2.SequentialCommandGroup(
                Avancer(base_pilotable, -1, -0.3),
                ViserTirer(base_pilotable, stick, shooter, intake, vision),
            )
        )
        self.setName(self.__class__.__name__)