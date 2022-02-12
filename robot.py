#!/usr/bin/env python3
import wpilib
import commands2
from commands2._impl.button import JoystickButton

from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake

from commands.piloter import Piloter
from commands.avancer import Avancer
from commands.tourner import Tourner
from commands.prendreballon import PrendreBallon


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.intake = Intake()
        self.base_pilotable = BasePilotable()
        self.stick = wpilib.Joystick(0)
        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        JoystickButton(self.stick, 1).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 2).whenPressed(Tourner(self.base_pilotable, 45.0, 0.75))
        JoystickButton(self.stick, 3).whenPressed(Tourner(self.base_pilotable, -45.0, 0.75))
        JoystickButton(self.stick, 4).whenPressed(Avancer(self.base_pilotable, 1.0, 0.75))


if __name__ == '__main__':
    wpilib.run(Robot)
