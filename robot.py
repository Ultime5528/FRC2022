#!/usr/bin/env python3
import wpilib
import commands2
from commands2._impl.button import JoystickButton

from subsystems.visionhub import VisionHub
from subsystems.intake import Intake
from subsystems.basepilotable import BasePilotable
from commands.prendreballon import PrendreBallon
from commands.piloter import Piloter
from commands.viserhub import ViserHub


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("hub.py:main")

        self.intake = Intake()
        self.base_pilotable = BasePilotable()
        self.visionhub = VisionHub()
        self.stick = wpilib.Joystick(0)
        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        JoystickButton(self.stick, 3).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 4).whenPressed(ViserHub(self.base_pilotable, self.visionhub, 0))

if __name__ == "__main__":
    wpilib.run(Robot)
