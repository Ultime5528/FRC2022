import wpilib
import commands2
from commands2.button import JoystickButton

import properties
from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from commands.grimpeur.grimperniveau2 import GrimperNiveau2
from commands.grimpeur.grimperniveau3 import GrimperNiveau3
from commands.grimpeur.grimperniveau4 import GrimperNiveau4
from commands.grimpeur.montercompletsecondaire import MonterCompletSecondaire
from commands.grimpeur.preparergrimper import PreparerGrimper
from commands.visercargo import ViserCargo, ViserCargoAvancer

from commands.monterintake import MonterIntake
from commands.sequenceprendre import SequencePrendre
from commands.viserprendre import ViserPrendre
from commands.visertirer import ViserTirer
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.basepilotable import BasePilotable

from subsystems.shooter import Shooter
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from LED import LEDController

from wpimath.geometry import Pose2d, Rotation2d
from commands.viserhub import ViserHub
from commands.shooter.manualshoot import ManualShoot
from commands.piloter import Piloter
from commands.avancer import Avancer
from commands.tourner import Tourner
from commands.prendreballon import PrendreBallon
from commands.suivretrajectoire import SuivreTrajectoire
from commands.descendreintake import DescendreIntake
from commands.arreterintake import ArreterIntake
from commands.shooter.interpolatedshoot import InterpolatedShoot
from commands.shooter.dashboardshoot import DashboardShoot
from commands.ejecterintake import EjecterIntake
from triggers.wrongcargotrigger import WrongCargoTrigger
from triggers.axistrigger import AxisTrigger
from commands.shooter.ejectershooter import EjecterShooter


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # CameraServer.launch("visionhub.py:main")
        # CameraServer.launch("visioncargo.py:main")
        self.stick = wpilib.Joystick(0)
        self.console_1 = wpilib.Joystick(1)
        self.console_2 = wpilib.Joystick(2)

        self.base_pilotable = BasePilotable()
        self.intake = Intake()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.shooter = Shooter()

        self.grimpeur_primaire = GrimpeurPrimaire()
        self.grimpeur_secondaire = GrimpeurSecondaire()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.led_controller = LEDController()
        #
        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))

        self.setup_buttons()

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

        wpilib.SmartDashboard.putData("Shoot", ManualShoot(self.shooter, self.intake, 3000, 3000))
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
        wpilib.SmartDashboard.putData("Shoot", ManualShoot(self.shooter, self.intake, 3000, 3000))
        wpilib.SmartDashboard.putData("Monter Intake", MonterIntake(self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("Interpolated Shoot", InterpolatedShoot(self.shooter, self.intake, self.vision_targets))
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

        wpilib.SmartDashboard.putData("2", GrimperNiveau2(self.grimpeur_primaire))
        wpilib.SmartDashboard.putData("3", GrimperNiveau3(self.grimpeur_primaire, self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("4", GrimperNiveau4(self.grimpeur_primaire, self.grimpeur_secondaire))
        wpilib.SmartDashboard.putData("Viser Cargo", ViserCargo(self.base_pilotable, self.vision_targets))

    def setup_buttons(self):
        # JOYSTICK
        JoystickButton(self.stick, 7).whenPressed(Piloter(self.base_pilotable, self.stick))
        JoystickButton(self.stick, 2).whenPressed(ViserTirer(self.base_pilotable, self.stick, self.shooter, self.intake, self.vision_targets))
        JoystickButton(self.stick, 3).whenPressed(ViserPrendre(self.base_pilotable, self.intake, self.vision_targets))

        # CONSOLE
        JoystickButton(self.console_1, 5).whenPressed(GrimperNiveau2(self.grimpeur_primaire))
        JoystickButton(self.console_1, 8).whenPressed(GrimperNiveau3(self.grimpeur_primaire, self.grimpeur_secondaire))
        JoystickButton(self.console_2, 3).whenPressed(GrimperNiveau4(self.grimpeur_primaire, self.grimpeur_secondaire))
        JoystickButton(self.console_1, 4).whenPressed(PreparerGrimper(self.grimpeur_primaire, self.grimpeur_secondaire))
        JoystickButton(self.console_1, 7).whenPressed(ViserTirer(self.base_pilotable, self.stick, self.shooter, self.intake, self.vision_targets))
        JoystickButton(self.console_2, 2).whenPressed(InterpolatedShoot(self.shooter, self.intake, self.vision_targets))
        #JoystickButton(self.console_1, 3).whenPressed(Exploser(self.led_controller))
        JoystickButton(self.console_1, 6).whenPressed(ViserPrendre(self.base_pilotable, self.intake, self.vision_targets))
        #JoystickButton(self.console_2, 1).whenPressed(ManualShoot())
        JoystickButton(self.console_1, 2).whenPressed(SequencePrendre(self.grimpeur_secondaire, self.intake))
        JoystickButton(self.console_1, 1).whenPressed(EjecterIntake(self.intake))
        AxisTrigger(self.console_1, 0, inverted=True).whenActive(MonterIntake(self.grimpeur_secondaire))
        AxisTrigger(self.console_1, 0, inverted=False).whenActive(DescendreIntake(self.grimpeur_secondaire))
        AxisTrigger(self.console_1, 1, inverted=False).whenActive(MonterIntake(self.grimpeur_secondaire))
        AxisTrigger(self.console_1, 1, inverted=True).whenActive(DescendreIntake(self.grimpeur_secondaire))


    def robotPeriodic(self) -> None:
        # try:
        commands2.CommandScheduler.getInstance().run()
        # except Exception as e:
        #     print(e)
        #     traceback.print_exc()


if __name__ == "__main__":
    # try:
    wpilib.run(Robot)
    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
