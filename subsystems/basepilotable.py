import wpilib
import wpilib.drive
import commands2
import rev


class BasePilotable(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # TODO correct mesurements
        self.x_wheelbase = 0.58 / 2
        self.y_wheelbase = 0.515 / 2

        self.motor_front_left = rev.CANSparkMax(0, rev.MotorType.kBrushless)
        self.motor_front_right = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.motor_front_left.restoreFactoryDefaults() 
        self.motor_front_right.restoreFactoryDefaults()

        self.drive = wpilib.drive.DifferentialDrive(self.motor_front_left, self.motor_front_right)


    def arcadeDrive(self, forwardSpeed: float, rotation: float) -> None:
        self.drive.arcadeDrive(forwardSpeed, rotation)
    
    