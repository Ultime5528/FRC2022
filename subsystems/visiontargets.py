import math
import time

import commands2
from networktables import NetworkTables
from pyfrc.physics.visionsim import VisionSim
from wpimath.geometry import Pose2d
from wpilib import RobotBase, Field2d


class VisionTargets(commands2.SubsystemBase):
    def __init__(self, basepilotable) -> None:
        super().__init__()
        self.hubNormxEntry = NetworkTables.getEntry("Vision/Hub/Norm_X")
        self.hubNormyEntry = NetworkTables.getEntry("Vision/Hub/Norm_Y")

        self.cargoNormxEntry = NetworkTables.getEntry("Vision/Cargo/Norm_X")
        self.cargoNormyEntry = NetworkTables.getEntry("Vision/Cargo/Norm_Y")
        self.cargoFoundEntry = NetworkTables.getEntry("Vision/Cargo/Found")

        if RobotBase.isSimulation():
            self.basepilotable = basepilotable
            x, y = 4, 1
            self.cargo_sim = VisionSim([VisionSim.Target(x, y,0,359)], 120, 0, 100)

            fakecargo = basepilotable.field.getObject("CARGO")
            fakecargo.setPose(Pose2d(x, y, 0))

    @property
    def hubNormX(self):
        return self.hubNormxEntry.getDouble(0)

    @property
    def hubNormY(self):
        return self.hubNormyEntry.getDouble(0)

    @property
    def cargoNormX(self):
        return self.cargoNormxEntry.getDouble(0)

    @property
    def cargoNormY(self):
        return self.cargoNormyEntry.getDouble(0)

    @property
    def cargoFound(self):
        return self.cargoFoundEntry.getBoolean(False)

    def simulationPeriodic(self):
        pose = self.basepilotable.odometry.getPose()
        targets = self.cargo_sim.compute(time.time(), pose.X(), pose.Y(), -pose.rotation().degrees())

        if targets:
            print(targets[0])
            if targets[0][0]:
                norm_x = targets[0][3] / 60
                norm_y = targets[0][2] / 100

                self.cargoNormxEntry.setDouble(norm_x)
                self.cargoNormyEntry.setDouble(norm_y)
                self.cargoFoundEntry.setBoolean(True)
            else:
                self.cargoFoundEntry.setBoolean(False)
        else:
            self.cargoFoundEntry.setBoolean(False)

