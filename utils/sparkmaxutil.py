import rev
from wpilib import Timer

import properties
from utils.logutil import reportError


def handleCANError(error: rev.REVLibError, message: str, motor: rev.CANSparkMax):
    if error != rev.REVLibError.kOk:
        reportError("CANError",
                "Error (" + error.toString() + ") on motor ID " + motor.getDeviceId() + " : " + message)

@staticmethod
def handleCANError(error: rev.REVLibError, message: str):
    if error != rev.REVLibError.kOk:
        reportError("CANError", "Error (" + error.toString() + ") : " + message)


@staticmethod
def configureMotor(motor: rev.CANSparkMax, brake: bool):
    handleCANError(motor.restoreFactoryDefaults(), "restoryFactoryDefaults", motor);
    handleCANError(motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake if brake else rev.CANSparkMax.IdleMode.kCoast), "setIdleMode", motor);
    handleCANError(motor.enableVoltageCompensation(properties.values.sparkmax_voltage_compensation), "enableVoltageCompensation", motor);
    handleCANError(motor.burnFlash(), "burnFlash", motor);
    handleCANError(motor.clearFaults(), "clearFaults", motor);
    Timer.delay(0.250);

@staticmethod
def configureFollower(motor: rev.CANSparkMax, leader: rev.CANSparkMax, brake: bool, inverted: bool=False):
    handleCANError(motor.restoreFactoryDefaults(), "restoryFactoryDefaults", motor);
    handleCANError(motor.setPeriodicFramePeriod(rev.CANSparkMax.PeriodicFrame.kStatus0, 1000), "set status0 rate", motor);
    handleCANError(motor.setPeriodicFramePeriod(rev.CANSparkMax.PeriodicFrame.kStatus1, 1000), "set status1 rate", motor);
    handleCANError(motor.setPeriodicFramePeriod(rev.CANSparkMax.PeriodicFrame.kStatus2, 1000), "set status2 rate", motor);
    handleCANError(motor.follow(leader, inverted), "follow", motor);
    configureMotor(motor, brake);