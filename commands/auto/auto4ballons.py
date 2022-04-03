import commands2
from wpilib import Joystick
from wpimath.geometry import Pose2d, Rotation2d

from commands.basepilotable.avancer import Avancer
from commands.basepilotable.suivretrajectoire import SuivreTrajectoire
from commands.intake.descendreintake import DescendreIntake
from commands.intake.monterintake import MonterIntake
from commands.intake.prendreballon import PrendreBallon
from commands.shooter.manualshoot import ManualShoot
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
            stick: Joystick,
            shooter: Shooter,
            intake: Intake,
            vision: VisionTargets,
            grimpeur_secondaire: GrimpeurSecondaire
    ):
        super().__init__(
            commands2.ParallelRaceGroup(
                commands2.WaitCommand(2.5),
                commands2.ParallelDeadlineGroup(
                    PrendreBallon(intake),

                    SuivreTrajectoire(base_pilotable,
                                      [Pose2d(1.1, 0.2, Rotation2d.fromDegrees(23))],
                                      0.2, reset=True, addRobotPose=True),
                    DescendreIntake(grimpeur_secondaire),
                )
            ),

            commands2.ParallelRaceGroup(
                # commands2.WaitCommand(10),
                commands2.ParallelDeadlineGroup(
                    ViserTirer(base_pilotable, stick, shooter, intake, vision),
                    MonterIntake(grimpeur_secondaire)
                ),
            ),
            commands2.ParallelRaceGroup(
                # commands2.WaitCommand(10),
                commands2.ParallelCommandGroup(
                    SuivreTrajectoire(base_pilotable,
                                      [Pose2d(5.8, -1, Rotation2d.fromDegrees(27))],
                                      0.3, addRobotPose=True),
                    commands2.SequentialCommandGroup(
                        DescendreIntake(grimpeur_secondaire),
                        PrendreBallon(intake),
                    )
                ),
            ),
            Avancer(base_pilotable, -1, -0.2),
            commands2.ParallelCommandGroup(
                MonterIntake(grimpeur_secondaire),
                ViserTirer(base_pilotable, stick, shooter, intake, vision),
            )

        )
        self.setName(self.__class__.__name__),
