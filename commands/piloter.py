from commands2 import CommandBase
import wpilib
from wpilib._wpilib import Joystick
from subsystems.basepilotable import BasePilotable


class Piloter(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, stick: wpilib.Joystick):
        super().__init__()

        self.stick = stick
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Piloter")

        

    def execute(self):
        self.base_pilotable.arcadeDrive(self.stick.getX(), self.stick.getY())