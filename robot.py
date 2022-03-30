import commands2
import wpilib
from commands2.button import JoystickButton
from wpimath.geometry import Pose2d, Rotation2d

from LED import LEDController
from commands.balayerballon import BalayerBallon
from commands.basepilotable.avancer import Avancer
from commands.basepilotable.piloter import Piloter
from commands.basepilotable.piloteraide import PiloterAide
from commands.basepilotable.suivretrajectoire import SuivreTrajectoire
from commands.basepilotable.tourner import Tourner
from commands.grimpeur.bougerprimaire import BougerPrimaire
from commands.grimpeur.bougersecondaire import BougerSecondaire
from commands.grimpeur.descendrecompletprimaire import DescendreCompletPrimaire
from commands.grimpeur.descendrecompletsecondaire import DescendreCompletSecondaire
from commands.grimpeur.grimperniveau2 import GrimperNiveau2
from commands.grimpeur.grimperniveau3 import GrimperNiveau3
from commands.grimpeur.grimperniveau4 import GrimperNiveau4
from commands.grimpeur.montercompletsecondaire import MonterCompletSecondaire
from commands.grimpeur.preparergrimper import PreparerGrimper
from commands.grimpeur.resetgrimpeurs import ResetGrimpeurs
from commands.intake.descendreintake import DescendreIntake
from commands.intake.monterintake import MonterIntake
from commands.intake.prendreballon import PrendreBallon
from commands.intake.sequenceprendre import SequencePrendre
from commands.sequencebalayer import SequenceBalayer
from commands.shooter.dashboardshoot import DashboardShoot
from commands.shooter.ejectershooter import EjecterShooter
from commands.shooter.interpolatedshoot import InterpolatedShoot
from commands.shooter.manualshoot import ManualShoot
from commands.vision.visercargo import ViserCargo
from commands.vision.visercargoavancer import ViserCargoAvancer
from commands.vision.viserhub import ViserHub
from commands.vision.visertirer import ViserTirer
from subsystems.basepilotable import BasePilotable
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets
from triggers.axistrigger import AxisTrigger
from utils.dashboard import put_command_on_dashboard


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # CameraServer.launch("visionhub.py:main")
        # CameraServer.launch("visioncargo.py:main")

        self.stick = wpilib.Joystick(0)
        self.console_1 = wpilib.Joystick(1)
        self.console_2 = wpilib.Joystick(2)

        self.base_pilotable = BasePilotable()
        self.intake = Intake()
        self.shooter = Shooter()
        self.grimpeur_primaire = GrimpeurPrimaire()
        self.grimpeur_secondaire = GrimpeurSecondaire()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.led_controller = LEDController()

        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))

        self.setup_triggers()
        self.setup_dashboard()

    def setup_triggers(self):
        # JOYSTICK
        JoystickButton(self.stick, 7).whenPressed(Piloter(self.base_pilotable, self.stick))
        JoystickButton(self.stick, 2).whenPressed(
            ViserTirer(self.base_pilotable, self.stick, self.shooter, self.intake, self.vision_targets))
        JoystickButton(self.stick, 3).whenPressed(ViserCargoAvancer(self.base_pilotable, self.vision_targets))
        JoystickButton(self.stick, 4).whenHeld(PiloterAide(self.base_pilotable, self.vision_targets, self.stick))

        # CONSOLE
        JoystickButton(self.console_1, 5).whenPressed(GrimperNiveau2(self.grimpeur_primaire))
        JoystickButton(self.console_1, 8).whenPressed(GrimperNiveau3(self.grimpeur_primaire, self.grimpeur_secondaire))
        JoystickButton(self.console_2, 3).whenPressed(GrimperNiveau4(self.grimpeur_primaire, self.grimpeur_secondaire))
        JoystickButton(self.console_1, 4).whenPressed(PreparerGrimper(self.grimpeur_primaire, self.grimpeur_secondaire))
        JoystickButton(self.console_1, 7).whenPressed(
            ViserTirer(self.base_pilotable, self.stick, self.shooter, self.intake, self.vision_targets))
        JoystickButton(self.console_2, 2).whenPressed(InterpolatedShoot(self.shooter, self.intake, self.vision_targets))
        # JoystickButton(self.console_1, 3).whenPressed(Exploser(self.led_controller))
        JoystickButton(self.console_1, 6).whenPressed(ViserCargoAvancer(self.base_pilotable, self.vision_targets))
        # JoystickButton(self.console_2, 1).whenPressed(ManualShoot())
        JoystickButton(self.console_1, 2).whenPressed(SequencePrendre(self.grimpeur_secondaire, self.intake))
        JoystickButton(self.console_1, 1).whenPressed(SequenceBalayer(self.grimpeur_secondaire, self.intake))
        AxisTrigger(self.console_1, 0, inverted=True).whenActive(MonterIntake(self.grimpeur_secondaire))
        AxisTrigger(self.console_1, 0, inverted=False).whenActive(DescendreIntake(self.grimpeur_secondaire))
        AxisTrigger(self.console_1, 1, inverted=False).whenActive(MonterIntake(self.grimpeur_secondaire))
        AxisTrigger(self.console_1, 1, inverted=True).whenActive(DescendreIntake(self.grimpeur_secondaire))
        # Pour une raison inconnue, le trigger doit être gardé comme attribut pour que les test fonctionnent.
        # self.trigger = WrongCargoTrigger(self.vision_targets)
        # self.trigger.whenActive(EjecterIntake(self.intake))

    def setup_dashboard(self):
        put_command_on_dashboard("Intake", MonterIntake(self.grimpeur_secondaire))
        put_command_on_dashboard("Intake", DescendreIntake(self.grimpeur_secondaire))
        put_command_on_dashboard("Intake", PrendreBallon(self.intake))
        put_command_on_dashboard("Intake", SequencePrendre(self.grimpeur_secondaire, self.intake))
        put_command_on_dashboard("Intake", BalayerBallon(self.intake))
        put_command_on_dashboard("Intake", SequenceBalayer(self.grimpeur_secondaire, self.intake))

        put_command_on_dashboard("Shooter", ManualShoot(self.shooter, self.intake, 3000, 3000))
        put_command_on_dashboard("Shooter", InterpolatedShoot(self.shooter, self.intake, self.vision_targets))
        put_command_on_dashboard("Shooter", DashboardShoot(self.shooter, self.intake))
        put_command_on_dashboard("Shooter", EjecterShooter(self.shooter, self.intake))

        put_command_on_dashboard("BasePilotable", Avancer(self.base_pilotable, -1, 0.15))
        put_command_on_dashboard("BasePilotable", Tourner(self.base_pilotable, -90, 0.1))
        put_command_on_dashboard("BasePilotable", SuivreTrajectoire(self.base_pilotable,
                                                                    [Pose2d(0, 0, Rotation2d.fromDegrees(0)),
                                                                     Pose2d(3, 1, Rotation2d.fromDegrees(0))],
                                                                    0.2,
                                                                    reset=True))

        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_max(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_clip(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", DescendreCompletPrimaire(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_middle(self.grimpeur_primaire))

        put_command_on_dashboard("GrimpeurSecondaire", MonterCompletSecondaire(self.grimpeur_secondaire))
        put_command_on_dashboard("GrimpeurSecondaire", DescendreCompletSecondaire(self.grimpeur_secondaire))
        put_command_on_dashboard("GrimpeurSecondaire", BougerSecondaire.to_aligner_bas(self.grimpeur_secondaire))
        put_command_on_dashboard("GrimpeurSecondaire", BougerSecondaire.to_next_level(self.grimpeur_secondaire))

        put_command_on_dashboard("Grimper", ResetGrimpeurs(self.grimpeur_primaire, self.grimpeur_secondaire))
        put_command_on_dashboard("Grimper", PreparerGrimper(self.grimpeur_primaire, self.grimpeur_secondaire))
        put_command_on_dashboard("Grimper", GrimperNiveau2(self.grimpeur_primaire))
        put_command_on_dashboard("Grimper", GrimperNiveau3(self.grimpeur_primaire, self.grimpeur_secondaire))
        put_command_on_dashboard("Grimper", GrimperNiveau4(self.grimpeur_primaire, self.grimpeur_secondaire))

        put_command_on_dashboard("Vision", ViserHub(self.base_pilotable, self.vision_targets))
        put_command_on_dashboard("Vision", ViserCargo(self.base_pilotable, self.vision_targets))
        put_command_on_dashboard("Vision", ViserCargoAvancer(self.base_pilotable, self.vision_targets))
        put_command_on_dashboard("Vision", PiloterAide(self.base_pilotable, self.vision_targets, self.stick))

    def robotPeriodic(self) -> None:
        # TODO if FMS
        # try:
        commands2.CommandScheduler.getInstance().run()
        # except Exception as e:
        #     print(e)
        #     traceback.print_exc()


if __name__ == "__main__":
    wpilib.run(Robot)
