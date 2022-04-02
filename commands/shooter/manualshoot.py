from commands.shooter.abstractshoot import AbstractShoot
from subsystems.intake import Intake
from subsystems.shooter import Shooter
import properties


class ManualShoot(AbstractShoot):
    @classmethod
    def bas(cls, shooter: Shooter, intake: Intake, setpoint: float, backspin_setpoint: float):
        cmd = cls(shooter, intake, properties.values.shooter_speed_bas, properties.values.shooter_backspin_speed_bas)
        cmd.setName(cmd.getName() + " bas")
        return cmd

    def __init__(self, shooter: Shooter, intake: Intake, setpoint: float, backspin_setpoint: float):
        super().__init__(shooter, intake)
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def shoot(self) -> None:
        self.shooter.shoot(self.setpoint, self.backspin_setpoint)
