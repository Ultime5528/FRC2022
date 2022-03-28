from typing import List

import commands2
from wpimath.geometry import Pose2d, Transform2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

import properties
from subsystems.basepilotable import BasePilotable


class SuivreTrajectoire(commands2.CommandBase):
    maxVelocity = 10
    maxAcceleration = 10

    def __init__(
        self,
        basePilotable: BasePilotable,
        waypoints: List[Pose2d],
        speed: float,
        reset: bool = False,
        addRobotPose: bool = False,
    ) -> None:
        super().__init__()
        self.waypoints = waypoints
        self.setName("SuivreTrajectoire")
        self.basePilotable = basePilotable
        self.addRequirements(basePilotable)
        self.speed = speed

        self.reset = reset
        self.addRobotPose = addRobotPose

        if not self.addRobotPose:
            self.trajectory = TrajectoryGenerator.generateTrajectory(
                self.waypoints, TrajectoryConfig(self.maxAcceleration, self.maxVelocity)
            )
            if self.reset:
                transformation = Transform2d(self.waypoints[0], Pose2d())
                self.trajectory = self.trajectory.transformBy(transformation)

            self.states = self.trajectory.states()

    def initialize(self) -> None:
        if self.reset:
            self.basePilotable.resetOdometry()

        if self.addRobotPose:
            self.trajectory = TrajectoryGenerator.generateTrajectory(
                [self.basePilotable.getPose2D(), *self.waypoints],
                TrajectoryConfig(self.maxAcceleration, self.maxVelocity),
            )
            self.states = self.trajectory.states()
        self.index = 0
        self.basePilotable.getField().getObject("traj").setTrajectory(self.trajectory)

    def execute(self) -> None:
        currentPose = self.basePilotable.getPose()

        while (
            self.index < (len(self.states) - 1)
            and currentPose.translation().distance(self.states[self.index].pose.translation())
            <= properties.values.trajectoire_vue_avant
        ):
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
