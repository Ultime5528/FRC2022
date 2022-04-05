import properties
from commands.shooter.abstractshoot import AbstractShoot
from subsystems.intake import Intake
from subsystems.shooter import Shooter


class DashboardShoot(AbstractShoot):
    def __init__(self, shooter: Shooter, intake: Intake):
        super().__init__(shooter, intake)

    def shoot(self):
        self.shooter.shoot(
            properties.values.shooter_speed, properties.values.shooter_backspin_speed
        )
