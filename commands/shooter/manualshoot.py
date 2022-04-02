import properties
from commands.shooter.abstractshoot import AbstractShoot
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from utils.properties import FloatProperty, to_callable


class ManualShoot(AbstractShoot):
    @classmethod
    def bas(cls, shooter: Shooter, intake: Intake):
        cmd = cls(shooter, intake,
                  lambda: properties.values.shooter_bas_speed,
                  lambda: properties.values.shooter_bas_backspin_speed)
        cmd.setName(cmd.getName() + " bas")
        return cmd

    def __init__(self, shooter: Shooter, intake: Intake, setpoint: FloatProperty, backspin_setpoint: FloatProperty):
        super().__init__(shooter, intake)
        self.get_setpoint = to_callable(setpoint)
        self.get_backspin_setpoint = to_callable(backspin_setpoint)

    def shoot(self) -> None:
        self.shooter.shoot(self.get_setpoint(), self.get_backspin_setpoint())
