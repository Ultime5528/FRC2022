import wpilib
import commands2


class Intake(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # Motors
        self.intakeMotor1 = wpilib.VictorSP(1)
        self.intakeMotor2 = wpilib.VictorSP(2)
        self.intakeToShooter = wpilib.VictorSP(3)
        # Sensors
        self.intakeSensor = wpilib.DigitalInput(1)
        self.shooterSensor = wpilib.DigitalInput(2)



