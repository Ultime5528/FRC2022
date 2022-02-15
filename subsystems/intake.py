import wpilib
import commands2
from wpilib import RobotBase


class Intake(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # Motors
        self.intakeMotor = wpilib.VictorSP(1)
        # Sensors
        # TODO trouver bon ports
        self.sensorShooter = wpilib.DigitalInput(5)
        self.sensorIntake = wpilib.DigitalInput(6)

    def HasBallIntake(self) -> bool:
        return self.sensorIntake.get()

    def HasBallShooter(self) -> bool:
        return self.sensorShooter.get()
