import math

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
        x = interpoler(self.stick.getX())
        y = interpoler(self.stick.getY())

        ori = math.atan2(y, x)
        mag = x**2+y**2

        vori = self.vision.optimalCargoOrientation()

        if vori:
            ori = (1 - properties.values.aide_pilotage_orientation_influence) * ori \
                 + properties.values.aide_pilotage_orientation_influence * vori

        forward = -mag * math.sin(ori)
        turn = mag * math.cos(ori)

        if self.vision.hasRightCargoNear:
            forward = min(forward, properties.values.aide_pilotage_slow_factor)

        self.base_pilotable.arcadeDrive(forward, turn)
