from commands2 import CommandBase
import wpilib
from subsystems.basepilotable import BasePilotable


class Piloter(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, stick: wpilib.Joystick):
        super().__init__()

        self.stick = stick
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Piloter")

    def execute(self):
        self.base_pilotable.arcadeDrive(self.stick.getY()*-1, self.stick.getX())
