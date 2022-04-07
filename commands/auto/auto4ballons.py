import commands2
from wpilib import Joystick
from wpimath.geometry import Pose2d, Rotation2d

from commands.basepilotable.avancer import Avancer
from commands.basepilotable.suivretrajectoire import SuivreTrajectoire
from commands.grimpeur.resetgrimpeurs import ResetGrimpeurs
from commands.intake.descendreintake import DescendreIntake
from commands.intake.monterintake import MonterIntake
from commands.intake.prendreballon import PrendreBallon
from commands.shooter.interpolatedshoot import InterpolatedShoot
from commands.shooter.manualshoot import ManualShoot
from commands.vision.visertirer import ViserTirer
from subsystems.basepilotable import BasePilotable
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets


class Auto4Ballons(commands2.SequentialCommandGroup):
    def __init__(
            self,
            base_pilotable: BasePilotable,
            stick: Joystick,
            shooter: Shooter,
            intake: Intake,
            vision: VisionTargets,
            grimpeur_primaire: GrimpeurPrimaire,
            grimpeur_secondaire: GrimpeurSecondaire
    ):
        super().__init__(
            commands2.ParallelRaceGroup(
                commands2.WaitCommand(2.5),
                commands2.ParallelDeadlineGroup(
                    PrendreBallon(intake),
                    SuivreTrajectoire(base_pilotable,
                                      [Pose2d(1.8, 0.1, Rotation2d.fromDegrees(10))],
                                      0.2, reset=True, addRobotPose=True),
                    commands2.SequentialCommandGroup(
                        ResetGrimpeurs(grimpeur_primaire, grimpeur_secondaire),
                        DescendreIntake(grimpeur_secondaire),
                    )
                )
            ),

            commands2.ParallelRaceGroup(
                # commands2.WaitCommand(10),
                commands2.ParallelDeadlineGroup(
                    # ViserTirer(base_pilotable, stick, shooter, intake, vision),
                    InterpolatedShoot(shooter, intake, vision)
                ),
            ),
            commands2.ParallelRaceGroup(
                # commands2.WaitCommand(10),
                commands2.ParallelCommandGroup(
                    SuivreTrajectoire(base_pilotable,
                                      [Pose2d(5.8, -1, Rotation2d.fromDegrees(27))],
                                      0.5, addRobotPose=True),
                    commands2.SequentialCommandGroup(
                        DescendreIntake(grimpeur_secondaire),
                        PrendreBallon(intake),
                    )
                ),
            ),
            SuivreTrajectoire(base_pilotable,
                              [Pose2d(4, -1.5, Rotation2d.fromDegrees(8))],
                              -0.5, addRobotPose=True, reversed=True),
            commands2.ParallelCommandGroup(
                MonterIntake(grimpeur_secondaire),
                # InterpolatedShoot(shooter, intake, vision),
                ViserTirer(base_pilotable, stick, shooter, intake, vision)
            )

        )
        self.setName(self.__class__.__name__),
