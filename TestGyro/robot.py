import commands2
import wpilib
import navx
from wpilib import SPI, SmartDashboard


class TestGyro(commands2.TimedCommandRobot):
    def robotInit(self):
        self.gyro = wpilib.ADXRS450_Gyro()
        self.gyro2 = navx.AHRS(SPI.Port.kMXP)

    def teleopInit(self):
        self.gyro.reset()
        self.gyro2.reset()

    def teleopPeriodic(self):
        SmartDashboard.putBoolean("IMU_Connected", self.gyro2.isConnected())
        SmartDashboard.putBoolean("IMU_IsCalibrating", self.gyro2.isCalibrating())
        SmartDashboard.putNumber("IMU_Yaw", self.gyro2.getYaw())
        SmartDashboard.putNumber("IMU_Pitch", self.gyro2.getPitch())
        SmartDashboard.putNumber("IMU_Roll", self.gyro2.getRoll())

        SmartDashboard.putNumber("IMU_CompassHeading", self.gyro2.getCompassHeading())

        SmartDashboard.putNumber("IMU_FusedHeading", self.gyro2.getFusedHeading())
        SmartDashboard.putNumber("Wold accel y", self.gyro2.getWorldLinearAccelY())
        SmartDashboard.putNumber("Wold accel x", self.gyro2.getWorldLinearAccelX())
        SmartDashboard.putNumber("Wold accel z", self.gyro2.getWorldLinearAccelZ())

        SmartDashboard.putNumber("rotation", self.gyro.getRotation2d().degrees())


if __name__ == "__main__":
    wpilib.run(TestGyro)
