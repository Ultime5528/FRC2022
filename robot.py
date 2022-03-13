import wpilib
import commands2
from commands2.button import JoystickButton

import properties
from commands.alignergrimpeur import AlignerGrimpeur
from commands.descendresecondaire import DescendreSecondaire
from commands.interpolatedshoot import InterpolatedShoot
from commands.monterintake import MonterIntake
from commands.montersecondaire import MonterSecondaire
from commands.monterprimaire import MonterPrimaire
from commands.descendreprimaire import DescendrePrimaire
from commands.arreterintake import ArreterIntake
from commands.ejecterintake import EjecterIntake
from commands.sequenceprendre import SequencePrendre
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.basepilotable import BasePilotable
from subsystems.shooter import Shooter
from subsystems.grimpeur import Grimpeur
from LED import LEDController

from wpimath.geometry import Pose2d, Rotation2d

from commands.viserhub import ViserHub
from commands.manualshoot import ManualShoot
from commands.piloter import Piloter
from commands.avancer import Avancer
from commands.tourner import Tourner
from commands.prendreballon import PrendreBallon
from commands.suivretrajectoire import SuivreTrajectoire
from commands.ejecterintake import EjecterIntake
from commands.descendreintake import DescendreIntake
from commands.arreterintake import ArreterIntake
from commands.interpolatedShoot import InterpolatedShoot
from commands.dashboardShoot import DashboardShoot
from utils.cameraserver import CameraServer
from commands.ejectershooter import EjecterShooter
import traceback

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # CameraServer.launch("visionhub.py:main")
        # CameraServer.launch("visioncargo.py:main")
        self.stick = wpilib.Joystick(0)
        self.base_pilotable = BasePilotable()
        self.intake = Intake()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.shooter = Shooter()
        self.grimpeur = Grimpeur()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.led_controller = LEDController()

        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))

        JoystickButton(self.stick, 1).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 2).whenPressed(Tourner(self.base_pilotable, 180.0, 0.50))
        JoystickButton(self.stick, 3).whenPressed(Tourner(self.base_pilotable, -90.0, 0.75))
        JoystickButton(self.stick, 4).whenPressed(Avancer(self.base_pilotable, 0.5, 0.75))
        JoystickButton(self.stick, 5).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        JoystickButton(self.stick, 6).whenPressed(EjecterIntake(self.intake))
        JoystickButton(self.stick, 7).whenPressed(PrendreBallon(self.intake))
        JoystickButton(self.stick, 12).whenPressed(ArreterIntake(self.intake))

        JoystickButton(self.stick, 3).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 4).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        wpilib.SmartDashboard.putData("Suivre Trajectoire",
                                      SuivreTrajectoire(self.base_pilotable,
                                                        [
                                                            Pose2d(0, 0, Rotation2d.fromDegrees(0)),
                                                            Pose2d(6, 6, Rotation2d.fromDegrees(90)),
                                                            Pose2d(12, 12, Rotation2d.fromDegrees(0)),
                                                            Pose2d(18, 6, Rotation2d.fromDegrees(-90)),
                                                            Pose2d(0, 0, Rotation2d.fromDegrees(180)),
                                                            ], speed=0.55))

        wpilib.SmartDashboard.putData("Monter Primaire", MonterPrimaire(self.grimpeur, lambda: properties.values.grimpeur_enconder_monter))
        wpilib.SmartDashboard.putData("Shoot", ManualShoot(self.shooter, 3000, 3000))
        wpilib.SmartDashboard.putData("Descendre Primaire", DescendrePrimaire(self.grimpeur))
        wpilib.SmartDashboard.putData("Descendre Secondaire", DescendreSecondaire(self.grimpeur))
        wpilib.SmartDashboard.putData("Monter Intake", MonterIntake(self.grimpeur))
        wpilib.SmartDashboard.putData("Interpolated Shoot", InterpolatedShoot(self.shooter, self.vision_targets))
        wpilib.SmartDashboard.putData("Descendre Intake", DescendreIntake(self.grimpeur))
        wpilib.SmartDashboard.putData("Arreter Intake", ArreterIntake(self.intake))
        wpilib.SmartDashboard.putData("Ejecter Intake", EjecterIntake(self.intake))
        wpilib.SmartDashboard.putData("Speed Testing Shoot", DashboardShoot(self.shooter))
        wpilib.SmartDashboard.putData("Shooter Eject", EjecterShooter(self.shooter))
        wpilib.SmartDashboard.putData("Sequence Prendre", SequencePrendre(self.grimpeur, self.intake))
        wpilib.SmartDashboard.putData("Aligner Grimpeur", AlignerGrimpeur(self.grimpeur))

    def robotPeriodic(self) -> None:
        try:
            commands2.CommandScheduler.getInstance().run()
        except Exception as e:
            print(e)
            traceback.print_exc()

if __name__ == "__main__":
    wpilib.run(Robot)
