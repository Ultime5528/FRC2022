
from typing import List
import commands2
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpilib.geometry import Pose2d, Translation2d
import math
import properties
from subsystems.basepilotable import BasePilotable


class SuivreTrajectoire(commands2.CommandBase):
    maxVelocity = 10
    maxAcceleration = 10

    def __init__(self, drive: BasePilotable, waypoints: List[Pose2d], speed: float) -> None:
        super().__init__()
        self.drive = drive
        config = TrajectoryConfig(self.maxAcceleration, self.maxVelocity)
        self.trajectory = TrajectoryGenerator.generateTrajectory(waypoints, config)
        self.speed = speed
        self.states = self.trajectory.states()
        self.angleInitial = self.trajectory.states()[0].pose.rotation()

    def initialize(self) -> None:
        self.drive.resetOdometry()
        self.index = 0

    def execute(self) -> None:
        while (self.index < len(self.states) and self.drive.odometry.getPose().translation().distance(
                self.states[self.index].pose.translation()) <= 0.25):
            self.index += 1

        poseInit = self.states[self.index].pose
        poseDest = self.states[self.index + 1].pose
        moveX = poseDest.X() - poseInit.X()
        moveY = poseDest.Y() - poseInit.Y()
        errorDegres = 90 - math.degrees(math.atan(moveX / moveY))

        correction = properties.trajectoire_angle_p * errorDegres
        self.drive.BasePilotable.tankDrive(self.speed + correction, self.speed - correction)










    def isFinished(self) -> bool:
        return self.index > len(self.states)

    def end(self, interrupted: bool) -> None:
        self.drive.driveCartesian(0, 0, 0)

