import commands2
from networktables import NetworkTables
from pyfrc.physics.visionsim import VisionSim
from wpilib import RobotBase


class VisionTargets(commands2.SubsystemBase):
     def __init__(self, basepilotable) -> None:
        self.cargoNormxEntry = NetworkTables.getEntry("Vision/Cargo/Norm_X")
        self.cargoNormyEntry = NetworkTables.getEntry("Vision/Cargo/Norm_Y")

        if RobotBase.isSimulation():
            self.basepilotable = basepilotable
            self.cargo_sim = VisionSim([VisionSim.Target(23,53,0,360)], 120, 0, 100)

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

    def simulationPeriodic(self):
        pose = self.basepilotable.odometry.getPose()
        targets = self.cargo_sim.compute(pose.X(), pose.Y(), pose.rotation())

        norm_x = targets[0][2] / 120
        norm_y = targets[0][3] / 100

        self.cargoNormxEntry.setDouble(norm_x)
        self.cargoNormxEntry.setDouble(norm_y)