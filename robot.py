import wpilib
import commands2
from commands2.button import JoystickButton

from commands.descendresecondaire import DescendreSecondaire
from commands.monterintake import MonterIntake
from commands.monterprimaire import MonterPrimaire
from commands.descendprimaire import DescendPrimaire
from commands.arreterintake import ArreterIntake
from commands.ejecterintake import EjecterIntake
from commands.visercargo import ViserCargo
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.basepilotable import BasePilotable
from commands.prendreballon import PrendreBallon
from subsystems.shooter import Shooter
from subsystems.grimpeur import Grimpeur

from wpimath.geometry import Pose2d, Rotation2d

from commands.viserhub import ViserHub
from commands.manualShoot import Shoot
from commands.piloter import Piloter
from commands.avancer import Avancer
from commands.tourner import Tourner
from commands.prendreballon import PrendreBallon
from commands.suivretrajectoire import SuivreTrajectoire
from commands.interpolatedShoot import InterpolatedShoot
from commands.dashboardShoot import DashboardShoot
from commands.ejectershooter import EjecterShooter

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("visionhub.py:main")
        wpilib.CameraServer.launch("visioncargo.py:main")

        self.stick = wpilib.Joystick(0)

        self.intake = Intake()
        self.base_pilotable = BasePilotable()
        self.shooter = Shooter()
        self.grimpeur = Grimpeur()
        self.vision_targets = VisionTargets(self.base_pilotable)

        # self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        self.base_pilotable.setDefaultCommand(ViserHub(self.base_pilotable, self.vision_targets))

        JoystickButton(self.stick, 3).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 4).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        wpilib.SmartDashboard.putData("Suivre Trajectoire",
                                      SuivreTrajectoire(self.base_pilotable,
                                                        [
                                                           # Pose2d(0, 0, Rotation2d.fromDegrees(0)),
                                                           # Pose2d(2.5, 0.8, Rotation2d.fromDegrees(35)),
                                                           # Pose2d(5, 5, Rotation2d.fromDegrees(90)),
                                                           # Pose2d(7.5, 9.3, Rotation2d.fromDegrees(30)),
                                                           # Pose2d(10, 9.8, Rotation2d.fromDegrees(0)),
                                                           # Pose2d(12.5, 9, Rotation2d.fromDegrees(-30)),
                                                           # Pose2d(15, 5, Rotation2d.fromDegrees(-90)),
                                                           # Pose2d(12.5, 1.6, Rotation2d.fromDegrees(-150)),
                                                           # Pose2d(10, 1, Rotation2d.fromDegrees(180)),
                                                           # Pose2d(1, 0, Rotation2d.fromDegrees(180)),
                                                            Pose2d(0, 0, Rotation2d.fromDegrees(0)),
                                                            Pose2d(6, 6, Rotation2d.fromDegrees(90)),
                                                            Pose2d(12, 12, Rotation2d.fromDegrees(0)),
                                                            Pose2d(18, 6, Rotation2d.fromDegrees(-90)),
                                                            Pose2d(0, 0, Rotation2d.fromDegrees(180)),
                                                        ], speed=0.55))
        wpilib.SmartDashboard.putData("Shoot", Shoot(self.shooter, 3000, 3000))
        wpilib.SmartDashboard.putData("grimper", MonterPrimaire(self.grimpeur))
        wpilib.SmartDashboard.putData("descendre", DescendPrimaire(self.grimpeur))
        wpilib.SmartDashboard.putData("descendre secondaire", DescendreSecondaire(self.grimpeur))
        wpilib.SmartDashboard.putData("monter intake", MonterIntake(self.grimpeur))
        wpilib.SmartDashboard.putData("Interpolated Shoot", InterpolatedShoot(self.shooter, self.vision_targets, self.stick))
        wpilib.SmartDashboard.putData("Speed Testing Shoot", DashboardShoot(self.shooter))
        wpilib.SmartDashboard.putData("Eject Ball", EjecterShooter(self.shooter))


if __name__ == "__main__":
    wpilib.run(Robot)
