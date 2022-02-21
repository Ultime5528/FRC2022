import math

import wpilib.drive
import wpilib
from wpilib import RobotBase, RobotController
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor
from utils.sparkmaxsim import SparkMaxSim
from wpimath.kinematics import DifferentialDriveKinematics, DifferentialDriveOdometry
from wpilib.simulation import DifferentialDrivetrainSim, ADXRS450_GyroSim

from utils.subsystembase import SubsystemBase
import commands2
import rev

import ports


class BasePilotable(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # TODO correct measurements
        self.x_wheelbase = 0.58 / 2
        self.y_wheelbase = 0.515 / 2
        # Motors
        self.motor_left = rev.CANSparkMax(ports.basepilotable_left_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right = rev.CANSparkMax(ports.basepilotable_right_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_left.restoreFactoryDefaults()
        self.motor_right.restoreFactoryDefaults()
        self.motor_right.setInverted(True)
        self.drive = wpilib.drive.DifferentialDrive(self.motor_left, self.motor_right)
        self.addChild("DifferentialDrive", self.drive)
        self.motor_left_slave = rev.CANSparkMax(ports.basepilotable_left_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right_slave = rev.CANSparkMax(ports.basepilotable_right_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self.motor_left_slave.restoreFactoryDefaults()
        self.motor_right_slave.restoreFactoryDefaults()
        self.motor_left_slave.follow(self.motor_left)
        self.motor_right_slave.follow(self.motor_right)
        # Odometry
        self.encoder_left = self.motor_left.getEncoder()
        self.encoder_right = self.motor_right.getEncoder()
        self.gyro = wpilib.ADXRS450_Gyro()
        self.addChild("Gyro", self.gyro)

        if RobotBase.isSimulation():
            self.motor_left_sim = SparkMaxSim(self.motor_left)
            self.motor_right_sim = SparkMaxSim(self.motor_right)
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
        self.motor_left.set(speed)

    def rightDrive(self, speed: float) -> None:
        self.motor_right.set(speed)

    def simulationPeriodic(self):
        self.drive_sim.setInputs(
            self.motor_left.get() * RobotController.getInputVoltage(),
            -self.motor_right.get() * RobotController.getInputVoltage())
        self.drive_sim.update(0.02)
        self.motor_left_sim.setPosition(self.drive_sim.getLeftPosition())
        self.motor_left_sim.setVelocity(self.drive_sim.getLeftVelocity())
        self.motor_right_sim.setPosition(self.drive_sim.getRightPosition())
        self.motor_right_sim.setVelocity(self.drive_sim.getRightVelocity())
        self.gyro_sim.setAngle(-self.drive_sim.getHeading().degrees())

    def resetOdometry(self) -> None:
        self.encoder_left.setPosition(0)
        self.encoder_right.setPosition(0)
        self.gyro.reset()
        self.odometry.resetPosition(Pose2d(), Rotation2d.fromDegrees(0.0))

        if RobotBase.isSimulation():
            self.motor_left_sim.setPosition(0)
            self.motor_right_sim.setPosition(0)
            self.drive_sim.setPose(Pose2d())

    def getAngle(self):
        return -math.remainder(self.gyro.getAngle(), 360.0)

    def getAverageEncoderPosition(self):
        return (self.encoder_left.getPosition() + self.encoder_right.getPosition()) / 2

    def periodic(self):
        self.odometry.update(self.gyro.getRotation2d(), self.encoder_left.getPosition(), self.encoder_right.getPosition())
        self.field.setRobotPose(self.odometry.getPose())

