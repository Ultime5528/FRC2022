import wpilib
import commands2
from subsystems.shooter import Shooter


class Shoot(commands2.CommandBase):
    def __init__(self, shooter_subsystem: Shooter):
        super(self).__init__()
