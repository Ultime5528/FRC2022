import math

import wpilib.drive
import commands2
import rev
import wpilib
from wpilib import RobotBase, RobotController
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor
from utils.sparkmaxsim import SparkMaxSim
from wpimath.kinematics import DifferentialDriveKinematics, DifferentialDriveOdometry
from wpilib.simulation import DifferentialDrivetrainSim, ADXRS450_GyroSim

import commands2
import rev

import ports


class BasePilotable(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # TODO correct measurements
        self.x_wheelbase = 0.58 / 2
        self.y_wheelbase = 0.515 / 2
        # Motors
        self.motor_front_left = rev.CANSparkMax(0, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_front_right = rev.CANSparkMax(1, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_front_left.restoreFactoryDefaults()
        self.motor_front_right.restoreFactoryDefaults()
        self.motor_front_right.setInverted(True)
        self.drive = wpilib.drive.DifferentialDrive(self.motor_front_left, self.motor_front_right)
        self.motor_rear_left_slave = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_rear_right_slave = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_rear_left_slave.follow(self.motor_front_left)
        self.motor_rear_right_slave.follow(self.motor_front_right)
        self.motor_rear_left_slave.restoreFactoryDefaults()
        self.motor_rear_right_slave.restoreFactoryDefaults()
        # Odometry
        self.encoder_front_left = self.motor_front_left.getEncoder()
        self.encoder_front_right = self.motor_front_right.getEncoder()
        self.gyro = wpilib.ADXRS450_Gyro()

        if RobotBase.isSimulation():
            self.motor_front_left_sim = SparkMaxSim(self.motor_front_left)
            self.motor_front_right_sim = SparkMaxSim(self.motor_front_right)
            self.gyro_sim = ADXRS450_GyroSim(self.gyro)
            self.system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 1.5, 0.3)
            self.drive_sim = DifferentialDrivetrainSim(self.system, 0.64, DCMotor.NEO(4), 1.5, 0.08, [0.001, 0.001, 0.001, 0.1, 0.1, 0.005, 0.005])
            self.kinematics = DifferentialDriveKinematics(0.64)
            self.odometry = DifferentialDriveOdometry(self.gyro.getRotation2d())
            self.field = wpilib.Field2d()
            wpilib.SmartDashboard.putData("Field", self.field)

    def arcadeDrive(self, forwardSpeed: float, rotation: float) -> None:
        self.drive.arcadeDrive(forwardSpeed, rotation)

    def leftDrive(self, speed: float) -> None:
        self.motor_front_left.set(speed)

    def rightDrive(self, speed: float) -> None:
        self.motor_front_right.set(speed)

    def simulationPeriodic(self):
        self.drive_sim.setInputs(
            self.motor_front_left.get()*RobotController.getInputVoltage(),
            -self.motor_front_right.get()*RobotController.getInputVoltage())
        self.drive_sim.update(0.02)
        self.motor_front_left_sim.setPosition(self.drive_sim.getLeftPosition())
        self.motor_front_left_sim.setVelocity(self.drive_sim.getLeftVelocity())
        self.motor_front_right_sim.setPosition(self.drive_sim.getRightPosition())
        self.motor_front_right_sim.setVelocity(self.drive_sim.getRightVelocity())
        self.gyro_sim.setAngle(-self.drive_sim.getHeading().degrees())

    def resetOdometry(self) -> None:
        self.encoder_front_left.setPosition(0)
        self.encoder_front_right.setPosition(0)
        self.gyro.reset()
        self.odometry.resetPosition(Pose2d(), Rotation2d.fromDegrees(0.0))

        if RobotBase.isSimulation():
            self.motor_front_left_sim.setPosition(0)
            self.motor_front_right_sim.setPosition(0)
            self.drive_sim.setPose(Pose2d())

    def getAngle(self):
        return -math.remainder(self.gyro.getAngle(), 360.0)

    def getAverageEncoderPosition(self):
        return (self.encoder_front_left.getPosition() + self.encoder_front_right.getPosition()) / 2

    def periodic(self):
        self.odometry.update(self.gyro.getRotation2d(), self.encoder_front_left.getPosition(), self.encoder_front_right.getPosition())
        self.field.setRobotPose(self.odometry.getPose())

