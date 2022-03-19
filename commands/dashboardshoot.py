import commands2
import wpilib

from subsystems.shooter import Shooter
import properties
from subsystems.intake import Intake


class DashboardShoot(commands2.CommandBase):
    def __init__(self, shooter: Shooter, intake: Intake):
        super().__init__()
        self.setName("Dashboard Shoot")
        self.shooter = shooter
        self.intake = intake
        self.addRequirements(self.shooter, self.intake)
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()

    def execute(self) -> None:
        self.shooter.shoot(properties.values.shooter_speed, properties.values.shooter_backspin_speed)
        if self.shooter.atSetpoint():
            self.intake.activerConvoyeur()
        else:
            self.intake.stopConvoyeur()

        if not self.intake.hasBallIntake() and not self.intake.hasBallConvoyeur():
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= properties.values.shooter_end_time

    def end(self, interrupted: bool) -> None:
        self.shooter.disable()
        self.intake.stopConvoyeur()
