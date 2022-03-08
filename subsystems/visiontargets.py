import commands2
from networktables import NetworkTables
# from pyfrc.physics.visionsim import VisionSim
from wpimath.geometry import Pose2d
from wpilib import RobotBase, Timer

from subsystems.basepilotable import BasePilotable


class VisionTargets(commands2.SubsystemBase):
    def __init__(self, basepilotable: BasePilotable) -> None:
        super().__init__()
        self.hubNormxEntry = NetworkTables.getEntry("Vision/Hub/Norm_X")
        self.hubNormyEntry = NetworkTables.getEntry("Vision/Hub/Norm_Y")
        self.hubFoundEntry = NetworkTables.getEntry("Vision/Hub/Found")

        self.cargoNormxEntry = NetworkTables.getEntry("Vision/Cargo/Norm_X")
        self.cargoNormyEntry = NetworkTables.getEntry("Vision/Cargo/Norm_Y")
        self.cargoFoundEntry = NetworkTables.getEntry("Vision/Cargo/Found")

        if RobotBase.isSimulation():
            from pyfrc.physics.visionsim import VisionSim
            self.basepilotable = basepilotable

            x, y = 8, 6
            self.hub_target = VisionSim.Target(x, y,0,359)
            self.hub_sim = VisionSim([self.hub_target], 120, 0, 10)

            self.fakehub = basepilotable.getField().getObject("HUB")
            self.fakehub.setPose(Pose2d(x, y, 0))

            x, y = 4, 1
            self.cargo_target = VisionSim.Target(x, y,0,359)
            self.cargo_sim = VisionSim([self.cargo_target], 120, 0, 10)

            self.fakecargo = basepilotable.getField().getObject("CARGO")
            self.fakecargo.setPose(Pose2d(x, y, 0))

    @property
    def hubNormX(self):
        return self.hubNormxEntry.getDouble(0)

    @property
    def hubNormY(self):
        return self.hubNormyEntry.getDouble(0)

    @property
    def hubFound(self):
        return self.hubFoundEntry.getBoolean(False)

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
        fakehubpose = self.fakehub.getPose()
        self.hub_target.x = fakehubpose.X()
        self.hub_target.y = fakehubpose.Y()

        fakecargopose = self.fakecargo.getPose()
        self.cargo_target.x = fakecargopose.X()
        self.cargo_target.y = fakecargopose.Y()

        pose = self.basepilotable.getPose()

        hubs = self.hub_sim.compute(Timer.getFPGATimestamp(), pose.X(), pose.Y(), pose.rotation().radians())

        if hubs:
            found, time, angle, distance = hubs[0]
            if hubs[0][0]:
                norm_x = angle / 60
                norm_y = distance / 10

                self.hubNormxEntry.setDouble(norm_x)
                self.hubNormyEntry.setDouble(norm_y)
                self.hubFoundEntry.setBoolean(True)
            else:
                self.hubFoundEntry.setBoolean(False)
        else:
            self.cargoFoundEntry.setBoolean(False)

        cargos = self.cargo_sim.compute(Timer.getFPGATimestamp(), pose.X(), pose.Y(), pose.rotation().radians())

        if cargos:
            found, time, angle, distance = cargos[0]
            if cargos[0][0]:
                norm_x = angle / 60
                norm_y = distance / 10

                self.cargoNormxEntry.setDouble(norm_x)
                self.cargoNormyEntry.setDouble(norm_y)
                self.cargoFoundEntry.setBoolean(True)
            else:
                self.cargoFoundEntry.setBoolean(False)
        else:
            self.cargoFoundEntry.setBoolean(False)

