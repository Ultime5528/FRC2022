import commands2
from networktables import NetworkTables
from pyfrc.physics.visionsim import VisionSim
from wpimath.geometry import Pose2d
from wpilib import RobotBase, Timer


class VisionTargets(commands2.SubsystemBase):
     def __init__(self, basepilotable) -> None:
        self.cargoNormxEntry = NetworkTables.getEntry("Vision/Cargo/Norm_X")
        self.cargoNormyEntry = NetworkTables.getEntry("Vision/Cargo/Norm_Y")
        self.cargoFoundEntry = NetworkTables.getEntry("Vision/Cargo/Found")

        if RobotBase.isSimulation():
            from pyfrc.physics.visionsim import VisionSim
            self.basepilotable = basepilotable
            x, y = 4, 1
            self.cargo_sim = VisionSim([VisionSim.Target(x, y,0,359)], 120, 0, 10)

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
        targets = self.cargo_sim.compute(Timer.getFPGATimestamp(), pose.X(), pose.Y(), pose.rotation().radians())

        if targets:
            found, time, angle, distance = targets[0]
            if targets[0][0]:
                norm_x = angle / 60
                norm_y = distance / 10

                self.cargoNormxEntry.setDouble(norm_x)
                self.cargoNormyEntry.setDouble(norm_y)
                self.cargoFoundEntry.setBoolean(True)
            else:
                self.cargoFoundEntry.setBoolean(False)
        else:
            self.cargoFoundEntry.setBoolean(False)

