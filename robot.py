#!/usr/bin/env python3
import wpilib
import commands2
from subsystems.basepilotable import BasePilotable
from subsystems.shooter import Shooter

from commands.piloter import Piloter
from commands.shoot import Shoot


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.base_pilotable = BasePilotable()
        self.shooter = Shooter()
        self.stick = wpilib.Joystick(0)
        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))
        wpilib.SmartDashboard.putData("Shoot", Shoot(self.shooter, self.stick, 3000, 3000))

if __name__ == "__main__":
    wpilib.run(Robot)
