import wpilib
import commands2
from commands2.button import JoystickButton

import properties
from commands.bougersecondaire import BougerSecondaire
from commands.descendrecompletsecondaire import DescendreCompletSecondaire
from commands.grimper2e import Grimper2e
from commands.grimpeur3eme import Grimpeur3eme
from commands.grimpeur4eme import Grimpeur4eme
from commands.montercompletsecondaire import MonterCompletSecondaire
from commands.preparergrimper import PreparerGrimper
from commands.visercargo import ViserCargo

from commands.interpolatedshoot import InterpolatedShoot
from commands.monterintake import MonterIntake
from commands.bougerprimaire import BougerPrimaire
from commands.descendrecompletprimaire import DescendreCompletPrimaire
from commands.arreterintake import ArreterIntake
from commands.ejecterintake import EjecterIntake
from commands.sequenceprendre import SequencePrendre
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.basepilotable import BasePilotable

from subsystems.shooter import Shooter
from subsystems.grimpeurprincipal import GrimpeurPrincipal
from subsystems.grimpeursecondaire import GrimpeurSecondaire
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
from commands.interpolatedshoot import InterpolatedShoot
from commands.dashboardshoot import DashboardShoot
from commands.ejecterintake import EjecterIntake
from triggers.wrongcargotrigger import WrongCargoTrigger
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

        self.grimpeur_primaire = GrimpeurPrincipal()
        self.grimpeur_secondaire = GrimpeurSecondaire()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.led_controller = LEDController()
        #
        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        #
        # # JoystickButton(self.stick, 1).whenHeld(PrendreBallon(self.intake))
        # # JoystickButton(self.stick, 2).whenPressed(Tourner(self.base_pilotable, 180.0, 0.50))
        # # JoystickButton(self.stick, 3).whenPressed(Tourner(self.base_pilotable, -90.0, 0.75))
        # # JoystickButton(self.stick, 4).whenPressed(Avancer(self.base_pilotable, 0.5, 0.75))
        # # JoystickButton(self.stick, 5).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        # # JoystickButton(self.stick, 6).whenPressed(EjecterIntake(self.intake))
        # # JoystickButton(self.stick, 7).whenPressed(PrendreBallon(self.intake))
        # # JoystickButton(self.stick, 12).whenPressed(ArreterIntake(self.intake))
        # #
        # # JoystickButton(self.stick, 3).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 4).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))

        # Pour une raison inconnue, le trigger doit être gardé comme attribut pour que les test fonctionnent.
        self.trigger = WrongCargoTrigger(self.vision_targets)
        self.trigger.whenActive(EjecterIntake(self.intake))
        # WrongCargoTrigger(self.vision_targets).whenActive(EjecterIntake(self.intake))

        wpilib.SmartDashboard.putData("Shoot", ManualShoot(self.shooter, 3000, 3000))
        wpilib.SmartDashboard.putData("Suivre Traj",
                                      SuivreTrajectoire(self.base_pilotable,
                                                        [
                                                            Pose2d(0, 0, Rotation2d.fromDegrees(0)),
                                                            Pose2d(3, 1, Rotation2d.fromDegrees(0)),
                                                        ], 0.2, reset=True))

        wpilib.SmartDashboard.putData("BougerPrimaire max", BougerPrimaire(self.grimpeur_primaire, lambda: properties.values.grimpeur_primaire_hauteur_max))
        wpilib.SmartDashboard.putData("DescendreCompletPrimaire", DescendreCompletPrimaire(self.grimpeur_primaire))
        wpilib.SmartDashboard.putData("PreparerGrimper", PreparerGrimper(self.grimpeur_primaire, self.grimpeur_secondaire))

        wpilib.SmartDashboard.putData("BougerSecondaire Alignement", BougerSecondaire(self.grimpeur_secondaire, lambda: properties.values.grimpeur_secondaire_hauteur_alignement))
        wpilib.SmartDashboard.putData("MonterCompletSecondaire", MonterCompletSecondaire(self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("DescendreCompletSecondaire", DescendreCompletSecondaire(self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("Shoot", ManualShoot(self.shooter, 3000, 3000))
        wpilib.SmartDashboard.putData("Monter Intake", MonterIntake(self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("Interpolated Shoot", InterpolatedShoot(self.shooter, self.vision_targets))
        wpilib.SmartDashboard.putData("Descendre Intake", DescendreIntake(self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("Arreter Intake", ArreterIntake(self.intake))
        wpilib.SmartDashboard.putData("Dashboard Shoot", DashboardShoot(self.shooter, self.intake))
        wpilib.SmartDashboard.putData("Shooter Eject", EjecterShooter(self.shooter, self.intake))
        wpilib.SmartDashboard.putData("Sequence Prendre", SequencePrendre(self.grimpeur_secondaire, self.intake))
        wpilib.SmartDashboard.putData("Ejecter Intake", EjecterIntake(self.intake))
        wpilib.SmartDashboard.putData("Prendre Ballon", PrendreBallon(self.intake))
        wpilib.SmartDashboard.putData("Avancer", Avancer(self.base_pilotable, -1, 0.15))
        wpilib.SmartDashboard.putData("Tourner", Tourner(self.base_pilotable, -90, 0.1))
        wpilib.SmartDashboard.putData("Viser Hub", ViserHub(self.base_pilotable, self.vision_targets))
        wpilib.SmartDashboard.putData("2", Grimper2e(self.grimpeur_primaire))
        wpilib.SmartDashboard.putData("3", Grimpeur3eme(self.grimpeur_primaire, self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("4", Grimpeur4eme(self.grimpeur_primaire, self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("Viser Cargo", ViserCargo(self.base_pilotable, self.vision_targets))

    def robotPeriodic(self) -> None:
        try:
            commands2.CommandScheduler.getInstance().run()
        except Exception as e:
            print(e)
            traceback.print_exc()


if __name__ == "__main__":
    try:
        wpilib.run(Robot)
    except Exception as e:
        print(e)
        traceback.print_exc()
