import commands2
import wpilib

from subsystems.shooter import Shooter
from networktables import NetworkTables

import properties


class DashboardShoot(commands2.CommandBase):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.setName("Dashboard Shoot")
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self) -> None:
        self.shooter.shoot(properties.shooter_speed, properties.backspin_shooter_speed)

    def end(self, interrupted: bool) -> None:
        self.shooter.disable()
