import wpilib
import wpilib.drive
import commands2
import rev

# from wpilib import RobotBase
# from utils.sparkmaxsim import SparkMaxSim
# from wpimath.kinematics import DifferentialDriveKinematics

class BasePilotable(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # TODO correct mesurements
        self.x_wheelbase = 0.58 / 2
        self.y_wheelbase = 0.515 / 2
        # Motors
        self.motor_front_left = rev.CANSparkMax(0, rev.MotorType.kBrushless)
        self.motor_front_right = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.motor_front_left.restoreFactoryDefaults() 
        self.motor_front_right.restoreFactoryDefaults()
        self.drive = wpilib.drive.DifferentialDrive(self.motor_front_left, self.motor_front_right)
        # Odometry

        # self.gyro = wpilib.ADXRS450_Gyro()

     # if RobotBase.isSimulation()
        #     self.fl_motor_sim = SparkMaxSim(self.fl_motor)
        #     self.fr_motor_sim = SparkMaxSim(self.fr_motor)
        #     self.rl_motor_sim = SparkMaxSim(self.rl_motor)
        #     self.rr_motor_sim = SparkMaxSim(self.rr_motor)

    def arcadeDrive(self, forwardSpeed: float, rotation: float) -> None:
        self.drive.arcadeDrive(forwardSpeed, rotation)