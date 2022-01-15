from commands2 import CommandBase

import wpilib
from wpilib._wpilib import Joystick

from constants import Proprietes
from subsystems.basepilotable import BasePilotable


class Piloter(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, stick: wpilib.Joystick):
        super().__init__()

        self.stick = stick
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Piloter")

        

    def execute(self):
        if Proprietes.mode_pilotage == 'joystick':
            if self.stick.getRawButton(2):
                self.base_pilotable.deadzoneDriveCartesian(
                    Proprietes.pilotage_max_x * self.stick.getX(),
                    Proprietes.pilotage_max_y * -self.stick.getY(),
                    Proprietes.pilotage_max_z * self.stick.getZ()
                )