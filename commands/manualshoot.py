import commands2
from subsystems.shooter import Shooter


class ManualShoot(commands2.CommandBase):
    def __init__(self, shooter: Shooter, setpoint: float, backspin_setpoint: float):
        super().__init__()
        self.setName("Manual Shoot")
        self.shooter = shooter
        self.addRequirements(self.shooter)
        self.setpoint = setpoint
        self.backspin_setpoint = backspin_setpoint

    def execute(self) -> None:
        self.shooter.shoot(self.setpoint, self.backspin_setpoint)

    def end(self, interrupted: bool) -> None:
        self.shooter.disable()
