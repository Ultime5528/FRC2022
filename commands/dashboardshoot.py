import commands2
from subsystems.shooter import Shooter
import properties


class DashboardShoot(commands2.CommandBase):
    def __init__(self, shooter: Shooter):
        super().__init__()
        self.setName("Dashboard Shoot")
        self.shooter = shooter
        self.addRequirements(self.shooter)

    def execute(self) -> None:
        self.shooter.shoot(properties.values.shooter_speed, properties.values.shooter_backspin_speed)

    def end(self, interrupted: bool) -> None:
        self.shooter.disable()
