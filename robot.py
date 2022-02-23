import wpilib
import commands2
from commands2.button import JoystickButton

from commands.arreterintake import ArreterIntake
from commands.ejecterintake import EjecterIntake
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.basepilotable import BasePilotable
from commands.prendreballon import PrendreBallon
from subsystems.shooter import Shooter

from wpimath.geometry import Pose2d, Rotation2d

from commands.viserhub import ViserHub
from commands.shoot import Shoot
from commands.piloter import Piloter
from commands.avancer import Avancer
from commands.tourner import Tourner
from commands.prendreballon import PrendreBallon
from commands.suivretrajectoire import SuivreTrajectoire

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("visionhub.py:main")
        
        self.stick = wpilib.Joystick(0)
        
        self.intake = Intake()
        self.base_pilotable = BasePilotable()
        self.vision_targets = VisionTargets()
        self.shooter = Shooter()

        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        
        JoystickButton(self.stick, 1).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 2).whenPressed(Tourner(self.base_pilotable, 180.0, 0.50))
        JoystickButton(self.stick, 3).whenPressed(Tourner(self.base_pilotable, -90.0, 0.75))
        JoystickButton(self.stick, 4).whenPressed(Avancer(self.base_pilotable, 0.5, 0.75))
        JoystickButton(self.stick, 5).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        JoystickButton(self.stick, 6).whenPressed(EjecterIntake(self.intake))
        JoystickButton(self.stick, 7).whenPressed(PrendreBallon(self.intake))
        JoystickButton(self.stick, 12).whenPressed(ArreterIntake(self.intake))

        wpilib.SmartDashboard.putData("Shoot", Shoot(self.shooter, self.stick, 3000, 3000))
        wpilib.SmartDashboard.putData("suivre trajectoire",
                                      SuivreTrajectoire(self.base_pilotable,
                                                        [
                                                            Pose2d(0, 0, Rotation2d.fromDegrees(0)),
                                                            Pose2d(2, 5, Rotation2d.fromDegrees(90)),
                                                            Pose2d(5, 5, Rotation2d.fromDegrees(-90)),
                                                            Pose2d(5, 1, Rotation2d.fromDegrees(-90)),
                                                            Pose2d(7, 1, Rotation2d.fromDegrees(90)),
                                                        ], speed=0.65))


if __name__ == "__main__":
    wpilib.run(Robot)
