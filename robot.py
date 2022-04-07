import commands2
import wpilib
from commands2 import CommandBase
from commands2.button import JoystickButton
from wpilib import PowerDistribution

from LED import LEDController
from commands.auto.auto2ballons import Auto2Ballons
from commands.auto.auto4ballons import Auto4Ballons
from commands.basepilotable.piloter import Piloter
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
from commands.intake.sequenceprendre import SequencePrendre
from commands.sequencebalayer import SequenceBalayer
from commands.shooter.interpolatedshoot import InterpolatedShoot
from commands.shooter.manualshoot import ManualShoot
from commands.vision.visercargoavancer import ViserCargoAvancer
from commands.vision.viserhub import ViserHub
from commands.vision.visertirer import ViserTirer
from properties import clear_properties
from subsystems.basepilotable import BasePilotable
from subsystems.grimpeurprimaire import GrimpeurPrimaire
from subsystems.grimpeursecondaire import GrimpeurSecondaire
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.visiontargets import VisionTargets
from triggers.axistrigger import AxisTrigger
from utils.dashboard import put_command_on_dashboard


def when_pressed_dashboard(subsystem:str, command:CommandBase, stick:wpilib.Joystick, button:int, held:bool=False):
    if held:
        JoystickButton(stick, button).whenHeld(command)
    else:
        JoystickButton(stick, button).whenPressed(command)

    put_command_on_dashboard(subsystem, command)

    return command

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # CameraServer.launch("visionhub.py:main")
        # CameraServer.launch("visioncargo.py:main")

        try:
            import remoterepl
            self.remote_repl = remoterepl.RemoteREPL(self)
            print("RemoteREPL started !")
        except ModuleNotFoundError:
            wpilib.reportWarning("Package 'remoterepl' not installed")

        self.stick = wpilib.Joystick(0)
        self.console_1 = wpilib.Joystick(1)
        self.console_2 = wpilib.Joystick(2)

        self.base_pilotable = BasePilotable()
        self.intake = Intake()
        self.shooter = Shooter()
        self.grimpeur_primaire = GrimpeurPrimaire()
        self.grimpeur_secondaire = GrimpeurSecondaire()
        self.vision_targets = VisionTargets(self.base_pilotable)
        self.led_controller = LEDController(self.intake, self.shooter)

        self.pdp = PowerDistribution()

        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))

        self.setup_triggers()
        self.setup_dashboard()

        self.autoCommand: commands2.CommandBase = None
        self.autoChooser = wpilib.SendableChooser()
        self.autoChooser.setDefaultOption("Rien", None)
        self.autoChooser.addOption("4 Ballons", Auto4Ballons(self.base_pilotable,
                                                          self.stick, self.shooter,
                                                          self.intake, self.vision_targets, self.grimpeur_secondaire))
        self.autoChooser.addOption("2 Ballons", Auto2Ballons(self.base_pilotable,
                                                          self.stick, self.shooter,
                                                          self.intake, self.vision_targets, self.grimpeur_secondaire))

        wpilib.SmartDashboard.putData("ModeAutonome", self.autoChooser)

        clear_properties()

    def setup_triggers(self):
        # JOYSTICK
        when_pressed_dashboard("BasePilotable", Piloter(self.base_pilotable, self.stick),self.stick, 7)
        when_pressed_dashboard("Vision", ViserTirer(self.base_pilotable, self.stick, self.shooter, self.intake, self.vision_targets),self.stick, 2)
        shootbas = when_pressed_dashboard("Shooter", ManualShoot.bas(self.shooter, self.intake),self.stick, 4, True)
        viserhub = when_pressed_dashboard("Vision", ViserHub(self.base_pilotable, self.vision_targets),self.stick, 5)
        visercargoavancer = when_pressed_dashboard("Vision", ViserCargoAvancer(self.base_pilotable, self.vision_targets),self.stick, 3)
        when_pressed_dashboard("Shooter", ManualShoot(self.shooter, self.intake, 3750, 1600), self.stick, 6)

        # CONSOLE
        when_pressed_dashboard("Grimper", GrimperNiveau2(self.grimpeur_primaire),self.console_1, 5)
        when_pressed_dashboard("Grimper", GrimperNiveau3(self.grimpeur_primaire, self.grimpeur_secondaire),self.console_1, 8)
        when_pressed_dashboard("Grimper", GrimperNiveau4(self.grimpeur_primaire, self.grimpeur_secondaire),self.console_2, 3)
        when_pressed_dashboard("Grimper", PreparerGrimper(self.grimpeur_primaire, self.grimpeur_secondaire),self.console_1, 4)
        JoystickButton(self.console_1, 7).whenPressed(viserhub)
        when_pressed_dashboard("Shooter", InterpolatedShoot(self.shooter, self.intake, self.vision_targets),self.console_2, 2)
        when_pressed_dashboard("Grimper", ResetGrimpeurs(self.grimpeur_primaire, self.grimpeur_secondaire),self.console_1, 3)
        JoystickButton(self.console_1, 6).whenPressed(visercargoavancer)
        JoystickButton(self.console_2, 1).whenPressed(shootbas)
        when_pressed_dashboard("Intake", SequencePrendre(self.grimpeur_secondaire, self.intake),self.console_1, 2)
        when_pressed_dashboard("Intake", SequenceBalayer(self.grimpeur_secondaire, self.intake),self.console_1, 1)

        monterintake = put_command_on_dashboard("Intake", MonterIntake(self.grimpeur_secondaire))
        descendreintake = put_command_on_dashboard("Intake", DescendreIntake(self.grimpeur_secondaire))

        AxisTrigger(self.console_1, 0, inverted=False).whenActive(monterintake)
        AxisTrigger(self.console_1, 0, inverted=True).whenActive(descendreintake)
        AxisTrigger(self.console_1, 1, inverted=True).whenActive(monterintake)
        AxisTrigger(self.console_1, 1, inverted=False).whenActive(descendreintake)
        # Pour une raison inconnue, le trigger doit être gardé comme attribut pour que les test fonctionnent.
        # self.trigger = WrongCargoTrigger(self.vision_targets)
        # self.trigger.whenActive(EjecterIntake(self.intake))

    def setup_dashboard(self):
        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_max(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_clip(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", DescendreCompletPrimaire(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_middle(self.grimpeur_primaire))
        put_command_on_dashboard("GrimpeurPrimaire", BougerPrimaire.to_middle_lent(self.grimpeur_primaire))

        put_command_on_dashboard("GrimpeurSecondaire", MonterCompletSecondaire(self.grimpeur_secondaire))
        put_command_on_dashboard("GrimpeurSecondaire", DescendreCompletSecondaire(self.grimpeur_secondaire))
        put_command_on_dashboard("GrimpeurSecondaire", BougerSecondaire.to_aligner_bas(self.grimpeur_secondaire))
        put_command_on_dashboard("GrimpeurSecondaire", BougerSecondaire.to_next_level(self.grimpeur_secondaire))

        put_command_on_dashboard("Autonome", Auto4Ballons(self.base_pilotable,
                                                          self.stick, self.shooter,
                                                          self.intake, self.vision_targets, self.grimpeur_secondaire))

    def robotPeriodic(self) -> None:
        # TODO if FMS
        # try:
        commands2.CommandScheduler.getInstance().run()
        # except Exception as e:
        #     print(e)
        #     traceback.print_exc()
        wpilib.SmartDashboard.putNumber("Current Grimpeur Secondaire", self.pdp.getCurrent(9))

    def autonomousInit(self) -> None:
        self.autoCommand = self.autoChooser.getSelected()

        if self.autoCommand:
            self.autoCommand.schedule()

    def teleopInit(self) -> None:
        if self.autoCommand:
            self.autoCommand.cancel()

if __name__ == "__main__":
    wpilib.run(Robot)
