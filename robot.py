#!/usr/bin/env python3
import wpilib
import commands2
from commands2._impl.button import JoystickButton

from commands.prendreballon import PrendreBallon
from subsystems.basepilotable import BasePilotable
from commands.piloter import Piloter
from subsystems.intake import Intake


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("hub.py:main")
        # self.intake = Intake()
        # self.base_pilotable = BasePilotable()
        # self.stick = wpilib.Joystick(0)
        # self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        # JoystickButton(self.stick, 1).whenHeld(PrendreBallon(self.intake))

if __name__ == "__main__":
    wpilib.run(Robot)
