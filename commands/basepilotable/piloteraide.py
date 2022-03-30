import wpilib

import properties
from commands.basepilotable.piloter import interpoler
from subsystems.basepilotable import BasePilotable
from subsystems.visiontargets import VisionTargets
from utils.safecommandbase import SafeCommandBase


class PiloterAide(SafeCommandBase):
    def __init__(self, base_pilotable: BasePilotable, vision: VisionTargets, stick: wpilib.Joystick):
        super().__init__()
        self.stick = stick
        self.base_pilotable = base_pilotable
        self.vision = vision
        self.addRequirements(base_pilotable)

    def execute(self):
        forward = -interpoler(self.stick.getY())
        turn = interpoler(self.stick.getX())

        if self.vision.hasRightCargoNear:
            forward = min(forward, properties.values.aide_pilotage_slow_factor)

        self.base_pilotable.arcadeDrive(forward, turn)
