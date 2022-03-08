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
        self._motor_left = rev.CANSparkMax(ports.basepilotable_left_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self._motor_left.restoreFactoryDefaults()
        self._motor_left_follower = rev.CANSparkMax(ports.basepilotable_left_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self._motor_left_follower.restoreFactoryDefaults()
        self._motor_left_follower.follow(self._motor_left)
        self._motor_right = rev.CANSparkMax(ports.basepilotable_right_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self._motor_right.restoreFactoryDefaults()
        self._motor_right.setInverted(True)
        self._motor_right_follower = rev.CANSparkMax(ports.basepilotable_right_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self._motor_right_follower.restoreFactoryDefaults()
        self._motor_right_follower.follow(self._motor_right)
        self._drive = wpilib.drive.DifferentialDrive(self._motor_left, self._motor_right)

        self.addChild("DifferentialDrive", self._drive)
        # Odometry
        self._encoder_left = self._motor_left.getEncoder()
        self._encoder_right = self._motor_right.getEncoder()
        self._gyro = wpilib.ADXRS450_Gyro()
        self._odometry = DifferentialDriveOdometry(self._gyro.getRotation2d(), initialPose=Pose2d(5,5,0))
        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)
        self._left_encoder_offset = 0
        self._right_encoder_offset = 0
        self.addChild("Gyro", self._gyro)

        if RobotBase.isSimulation():
            self._motor_left_sim = SparkMaxSim(self._motor_left)
            self._motor_right_sim = SparkMaxSim(self._motor_right)
            self._gyro_sim = ADXRS450_GyroSim(self._gyro)
            self._system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 1.5, 0.3)
            self._drive_sim = DifferentialDrivetrainSim(self._system, 0.64, DCMotor.NEO(4), 1.5, 0.08, [0.001, 0.001, 0.001, 0.1, 0.1, 0.005, 0.005])
            
    def arcadeDrive(self, forwardSpeed: float, rotation: float) -> None:
        self._drive.arcadeDrive(forwardSpeed, rotation, False)

    def tankDrive(self, left: float, right: float) -> None:
        self._drive.tankDrive(left, right, False)

    def simulationPeriodic(self):
        self._drive_sim.setInputs(
            self._motor_left.get() * RobotController.getInputVoltage(),
            self._motor_right.get() * RobotController.getInputVoltage())
        self._drive_sim.update(0.02)
        self._motor_left_sim.setPosition(self._drive_sim.getLeftPosition() + self._left_encoder_offset)
        self._motor_left_sim.setVelocity(self._drive_sim.getLeftVelocity())
        self._motor_right_sim.setPosition(self._drive_sim.getRightPosition() + self._right_encoder_offset)
        self._motor_right_sim.setVelocity(self._drive_sim.getRightVelocity())
        self._gyro_sim.setAngle(-self._drive_sim.getHeading().degrees())

    def resetOdometry(self) -> None:
        self._left_encoder_offset = self._encoder_left.getPosition()
        self._right_encoder_offset = self._encoder_right.getPosition()
        self._gyro.reset()
        self._odometry.resetPosition(Pose2d(), Rotation2d.fromDegrees(0.0))

        if RobotBase.isSimulation():
            self._drive_sim.setPose(Pose2d())

    def getAngle(self):
        return -math.remainder(self._gyro.getAngle(), 360.0)

    def getLeftEncoderPosition(self):
        return self._encoder_left.getPosition() - self._left_encoder_offset

    def getRightEncoderPosition(self):
        return self._encoder_right.getPosition() - self._right_encoder_offset

    def getAverageEncoderPosition(self):
        return (self.getLeftEncoderPosition() + self.getRightEncoderPosition()) / 2

    def getPose(self):
        return self._odometry.getPose()

    def getField(self):
        return self._field

    def periodic(self):
        self._odometry.update(self._gyro.getRotation2d(), self.getLeftEncoderPosition(), self.getRightEncoderPosition())
        self._field.setRobotPose(self._odometry.getPose())
