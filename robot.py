import wpilib
import commands2
from commands2.button import JoystickButton

from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets
from subsystems.basepilotable import BasePilotable
from commands.prendreballon import PrendreBallon
from subsystems.shooter import Shooter


from commands.viserhub import ViserHub
from commands.shoot import Shoot
from commands.piloter import Piloter
from commands.avancer import Avancer
from commands.tourner import Tourner
from commands.prendreballon import PrendreBallon


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

        wpilib.SmartDashboard.putData("Shoot", Shoot(self.shooter, self.stick, 3000, 3000))
        
if __name__ == "__main__":
    wpilib.run(Robot)
