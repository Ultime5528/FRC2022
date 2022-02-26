
from typing import List
import commands2
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.geometry import Pose2d
import properties
from subsystems.basepilotable import BasePilotable


class SuivreTrajectoire(commands2.CommandBase):
    maxVelocity = 10
    maxAcceleration = 10

    def __init__(self, basePilotable: BasePilotable, waypoints: List[Pose2d], speed: float) -> None:
        super().__init__()
        self.setName("SuivreTrajectoire")
        self.basePilotable = basePilotable
        self.addRequirements(basePilotable)
        config = TrajectoryConfig(self.maxAcceleration, self.maxVelocity)
        self.trajectory = TrajectoryGenerator.generateTrajectory(waypoints, config)
        self.speed = speed
        self.states = self.trajectory.states()
        # TODO
        # self.angleInitial = self.trajectory.states()[0].pose.rotation()

    def initialize(self) -> None:
        self.basePilotable.resetOdometry()
        self.index = 0
        self.basePilotable._field.getObject("traj").setTrajectory(self.trajectory)

    def execute(self) -> None:
        currentPose = self.basePilotable._odometry.getPose()

        while (self.index < (len(self.states) - 1) and currentPose.translation().distance(
                self.states[self.index].pose.translation()) <= properties.values.trajectoire_vue_avant):
            self.index += 1

        poseDest = self.states[self.index].pose
        # moveX = poseDest.X() - self.drive.odometry.getPose().X()
        # moveY = poseDest.Y() - self.drive.odometry.getPose().Y()
        # errorDegres = 90 - math.degrees(math.atan(moveX / moveY))

        error = currentPose.rotation() - poseDest.rotation()

        correction = properties.values.trajectoire_angle_p * error.degrees()
        self.basePilotable.tankDrive(self.speed + correction, self.speed - correction)

    def isFinished(self) -> bool:
        return self.index >= len(self.states) - 1

    def end(self, interrupted: bool) -> None:
        self.basePilotable.tankDrive(0, 0)

