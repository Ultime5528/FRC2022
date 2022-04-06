import math

import wpilib
from commands2 import CommandBase

from subsystems.basepilotable import BasePilotable
from utils.trapezoidalmotion import TrapezoidalMotion


class Tourner(CommandBase):
    def __init__(self, base_pilotable: BasePilotable, angle: float, speed: float):
        """
        Parameters
        ----------
        base_pilotable
        angle: Positif = antihoraire
        speed: SPEEED
        """
        super().__init__()
        self.motion = TrapezoidalMotion(
            start_position=0,
            end_position=angle,
            start_speed=0.1,
            end_speed=speed,
            accel=0.001
        )
        self.base_pilotable = base_pilotable
        self.addRequirements(base_pilotable)
        self.setName("Tourner")

    def initialize(self) -> None:
        self.base_pilotable.resetOdometry()

    def execute(self):
        # self.base_pilotable.arcadeDrive(-1, 1)
        # self.base_pilotable.arcadeDrive(0, math.copysign(self.speed, self.angle))
        self.motion.set_position(self.base_pilotable.getAngle())
        wpilib.SmartDashboard.putNumber("speed", self.motion.get_speed())
        self.base_pilotable.arcadeDrive(0, -self.motion.get_speed())

    def end(self, interrupted: bool) -> None:
        self.base_pilotable.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        return self.motion.is_finished()
