from commands.shooter.abstractshoot import AbstractShoot
from subsystems.intake import Intake
from subsystems.shooter import Shooter


class ManualShoot(AbstractShoot):
    def __init__(self, shooter: Shooter, intake: Intake, setpoint: float, backspin_setpoint: float):
        super().__init__(shooter, intake)
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def shoot(self) -> None:
        self.shooter.shoot(self.setpoint, self.backspin_setpoint)
