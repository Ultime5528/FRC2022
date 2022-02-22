#!/usr/bin/env python3
import wpilib
import commands2
from commands2.button import JoystickButton

from subsystems.visiontargets import VisionTargets
from subsystems.intake import Intake
from subsystems.basepilotable import BasePilotable
from commands.prendreballon import PrendreBallon
from subsystems.shooter import Shooter

from commands.piloter import Piloter
from commands.viserhub import ViserHub
from commands.interpolatedShoot import InterpolatedShoot
from commands.dashboardShoot import DashboardShoot
from commands.ejecterballonshooter import EjecterBallonShooter

class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("visionhub.py:main")
        
        self.stick = wpilib.Joystick(0)
        
        self.intake = Intake()
        self.base_pilotable = BasePilotable()
        self.vision_targets = VisionTargets()
        self.shooter = Shooter()

        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))

        JoystickButton(self.stick, 3).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 4).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        wpilib.SmartDashboard.putData("Interpolated Shoot", InterpolatedShoot(self.shooter, self.vision_targets, self.stick))
        wpilib.SmartDashboard.putData("Speed Testing Shoot", DashboardShoot(self.shooter))
        wpilib.SmartDashboard.putData("Eject Ball", EjecterBallonShooter(self.shooter))


if __name__ == "__main__":
    wpilib.run(Robot)
