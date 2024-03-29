import math

import navx
import rev
import wpilib
import wpilib.drive
from wpilib import RobotBase, RobotController
from wpilib.simulation import DifferentialDrivetrainSim, SimDeviceSim
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveOdometry
from wpimath.system import LinearSystemId
from wpimath.system.plant import DCMotor

import ports
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutil import configure_leader, configure_follower
from utils.subsystembase import SubsystemBase


class BasePilotable(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # Motors
        self._motor_left = rev.CANSparkMax(ports.basepilotable_left_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        configure_leader(self._motor_left, "brake")

        self._motor_left_follower = rev.CANSparkMax(ports.basepilotable_left_motor_2,
                                                    rev.CANSparkMax.MotorType.kBrushless)
        configure_follower(self._motor_left_follower, self._motor_left, "brake")

        self._motor_right = rev.CANSparkMax(ports.basepilotable_right_motor_1,
                                            rev.CANSparkMax.MotorType.kBrushless)
        configure_leader(self._motor_right, "brake")

        self._motor_right_follower = rev.CANSparkMax(ports.basepilotable_right_motor_2,
                                                     rev.CANSparkMax.MotorType.kBrushless)
        configure_follower(self._motor_right_follower, self._motor_right, "brake")

        self._drive = wpilib.drive.DifferentialDrive(self._motor_left, self._motor_right)
        self.addChild("DifferentialDrive", self._drive)

        # Odometry
        self._encoder_left = self._motor_left.getEncoder()
        self._encoder_right = self._motor_right.getEncoder()
        self._encoder_left.setPositionConversionFactor(0.0463)
        self._encoder_right.setPositionConversionFactor(0.0463)

        self._gyro = navx.AHRS(wpilib.SerialPort.Port.kMXP)
        self._odometry = DifferentialDriveOdometry(self._gyro.getRotation2d(), initialPose=Pose2d(5, 5, 0))
        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)
        self._left_encoder_offset = 0
        self._right_encoder_offset = 0
        self.addChild("Gyro", self._gyro)

        if RobotBase.isSimulation():
            self._motor_left_sim = SparkMaxSim(self._motor_left)
            self._motor_right_sim = SparkMaxSim(self._motor_right)
            gyro_sim_device = SimDeviceSim("navX-Sensor[1]")
            self._gyro_sim = gyro_sim_device.getDouble("Yaw")
            self._system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 5, 0.3)
            self._drive_sim = DifferentialDrivetrainSim(self._system, 0.64, DCMotor.NEO(4), 1.5, 0.08, [
                0.001, 0.001, 0.001, 0.1, 0.1, 0.005, 0.005
            ])

    def arcadeDrive(self, forward: float, rotation: float) -> None:
        self._drive.arcadeDrive(forward, rotation, False)

    def tankDrive(self, left: float, right: float) -> None:
        self._drive.tankDrive(left, right, False)

    def simulationPeriodic(self):
        self._drive_sim.setInputs(
            self._motor_left.get() * RobotController.getInputVoltage(),
            self._motor_right.get() * RobotController.getInputVoltage())
        self._drive_sim.update(0.02)
        self._motor_left_sim.setPosition(self._drive_sim.getLeftPosition() + self._left_encoder_offset)
        self._motor_left_sim.setVelocity(self._drive_sim.getLeftVelocity())
        self._motor_right_sim.setPosition(-self._drive_sim.getRightPosition() + self._right_encoder_offset)
        self._motor_right_sim.setVelocity(self._drive_sim.getRightVelocity())
        self._gyro_sim.set(-self._drive_sim.getHeading().degrees())

    def resetOdometry(self) -> None:
        self._left_encoder_offset = self._encoder_left.getPosition()
        self._right_encoder_offset = self._encoder_right.getPosition()
        self._odometry.resetPosition(Pose2d(), Rotation2d.fromDegrees(0.0))

        if RobotBase.isSimulation():
            self._drive_sim.setPose(Pose2d())
        else:
            self._gyro.reset()

    def getAngle(self):
        return -math.remainder(self._gyro.getAngle(), 360.0)

    def getLeftEncoderPosition(self):
        return self._encoder_left.getPosition() - self._left_encoder_offset

    def getRightEncoderPosition(self):
        return -(self._encoder_right.getPosition() - self._right_encoder_offset)

    def getAverageEncoderPosition(self):
        return (self.getLeftEncoderPosition() + self.getRightEncoderPosition()) / 2

    def getPose(self):
        return self._odometry.getPose()

    def getField(self):
        return self._field

    def periodic(self):
        self._odometry.update(self._gyro.getRotation2d(), self.getLeftEncoderPosition(), self.getRightEncoderPosition())
        self._field.setRobotPose(self._odometry.getPose())
        wpilib.SmartDashboard.putNumber("Left Encoder Position", self.getLeftEncoderPosition())
        wpilib.SmartDashboard.putNumber("Right Encoder Position", self.getRightEncoderPosition())
        wpilib.SmartDashboard.putNumber("Left Motor", self._motor_left.get())
        wpilib.SmartDashboard.putNumber("Right Motor", self._motor_right.get())

        # SmartDashboard.putBoolean("IMU_Connected", self._gyro.isConnected())
        # SmartDashboard.putBoolean("IMU_IsCalibrating", self._gyro.isCalibrating())
        # SmartDashboard.putNumber("IMU_Yaw", self._gyro.getYaw())
        # SmartDashboard.putNumber("IMU_Pitch", self._gyro.getPitch())
        # SmartDashboard.putNumber("IMU_Roll", self._gyro.getRoll())
        #
        # SmartDashboard.putNumber("IMU_CompassHeading", self._gyro.getCompassHeading())
        #
        # SmartDashboard.putNumber("IMU_FusedHeading", self._gyro.getFusedHeading())
        # SmartDashboard.putNumber("Wold accel y", self._gyro.getWorldLinearAccelY())
        # SmartDashboard.putNumber("Wold accel x", self._gyro.getWorldLinearAccelX())
        # SmartDashboard.putNumber("Wold accel z", self._gyro.getWorldLinearAccelZ())
        # SmartDashboard.putNumber("rotation", self._gyro.getRotation2d().degrees())
