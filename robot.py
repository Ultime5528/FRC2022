#!/usr/bin/env python3
import wpilib
import commands2


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        pass
        # self.base_pilotable = BasePilotable()
        # self.stick = wpilib.Joystick(0)
        # self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))


if __name__ == "__main__":
    wpilib.run(Robot)
