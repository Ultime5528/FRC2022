import wpilib
import commands2
from wpilib import RobotBase


class Intake(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # Motors
        self.intakeMotor = wpilib.VictorSP(1)





