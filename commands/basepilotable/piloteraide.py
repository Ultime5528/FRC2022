import wpilib
from commands2 import CommandBase

import properties
from piloter import interpoler
from subsystems.basepilotable import BasePilotable
from subsystems.visiontargets import VisionTargets


class PiloterAide(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, vision: VisionTargets, stick: wpilib.Joystick):
        super().__init__()

        self.stick = stick
        self.base_pilotable = base_pilotable
        self.vision = vision
        self.addRequirements(base_pilotable)
        self.addRequirements(vision)
        self.setName("Piloter avec aide")

    def execute(self):
        y = interpoler(self.stick.getX())
        x = -interpoler(self.stick.getY())

        if self.vision.hasRightCargoNear:
            y = min(y, properties.values.aide_pilotage_slow_factor)

        self.base_pilotable.arcadeDrive(y, x)
