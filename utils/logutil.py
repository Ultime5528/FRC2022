from wpilib import DriverStation


def reportError(errorType: str, message: str):
    DriverStation.reportError("[" + errorType + "] " + message, True)
