from dataclasses import dataclass

import commands2
import wpilib
from networktables import NetworkTables
from wpilib import RobotBase, Timer
from wpimath.geometry import Pose2d

import properties
from subsystems.basepilotable import BasePilotable


def is_red_alliance():
    return wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed


@dataclass
class Cargo:
    nx: float
    ny: float
    nw: float
    is_red: bool


class VisionTargets(commands2.SubsystemBase):
    def __init__(self, basepilotable: BasePilotable) -> None:
        super().__init__()
        self.hubNormxEntry = NetworkTables.getEntry("/Vision/Hub/Norm_X")
        self.hubNormyEntry = NetworkTables.getEntry("/Vision/Hub/Norm_Y")
        self.hubFoundEntry = NetworkTables.getEntry("/Vision/Hub/Found")

        self.cargoNormxEntry = NetworkTables.getEntry("/Vision/Cargo/Norm_X")
        self.cargoNormyEntry = NetworkTables.getEntry("/Vision/Cargo/Norm_Y")
        self.cargoNormwEntry = NetworkTables.getEntry("/Vision/Cargo/Norm_W")
        self.cargoIsRedEntry = NetworkTables.getEntry("/Vision/Cargo/IsRed")

        if RobotBase.isSimulation():
            from pyfrc.physics.visionsim import VisionSim
            self.basepilotable = basepilotable

            x, y = 8, 6
            self.hub_target = VisionSim.Target(x, y, 0, 359)
            self.hub_sim = VisionSim([self.hub_target], 120, 0, 10)

            self.fakehub = basepilotable.getField().getObject("HUB")
            self.fakehub.setPose(Pose2d(x, y, 0))

            x, y = 4, 1
            self.cargo_target = VisionSim.Target(x, y, 0, 359)
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
    def cargos(self):
        nxs = self.cargoNormxEntry.getDoubleArray([])
        nys = self.cargoNormyEntry.getDoubleArray([])
        nws = self.cargoNormwEntry.getDoubleArray([])
        is_reds = self.cargoIsRedEntry.getBooleanArray([])

        return [Cargo(nx, ny, nw, is_red) for nx, ny, nw, is_red in zip(nxs, nys, nws, is_reds)]

    @property
    def nearestCargo(self):
        is_red = is_red_alliance()
        good_cargos = [cargo for cargo in self.cargos if cargo.is_red == is_red]

        if good_cargos:
            return max(good_cargos, key=lambda x: x.nw)
        else:
            return None

    def hasRightCargoNear(self):
        for cargo in self.cargos:
            if cargo.is_red == is_red_alliance() \
                    and cargo.nw > properties.values.vision_cargo_normw_threshold \
                    and cargo.ny < properties.values.vision_cargo_normy_threshold:
                return True

        return False

    def hasWrongCargoNear(self):
        for cargo in self.cargos:
            if cargo.is_red != is_red_alliance() \
                    and cargo.nw > properties.values.vision_cargo_normw_threshold \
                    and cargo.ny < properties.values.vision_cargo_normy_threshold:
                return True

        return False

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
            if found:
                norm_x = angle / 60
                norm_y = distance / 10

                self.hubNormxEntry.setDouble(norm_x)
                self.hubNormyEntry.setDouble(norm_y)
                self.hubFoundEntry.setBoolean(True)
            else:
                self.hubFoundEntry.setBoolean(False)
        else:
            self.hubFoundEntry.setBoolean(False)

        cargos = self.cargo_sim.compute(Timer.getFPGATimestamp(), pose.X(), pose.Y(), pose.rotation().radians())

        reset_cargos = True

        if cargos:
            found, time, angle, distance = cargos[0]
            if found:
                norm_x = angle / 60
                norm_y = distance / 10

                self.cargoNormxEntry.setDoubleArray([norm_x])
                self.cargoNormyEntry.setDoubleArray([norm_y])
                self.cargoNormwEntry.setDoubleArray([norm_y / 2])
                self.cargoIsRedEntry.setBooleanArray([is_red_alliance()])
                reset_cargos = False

        if reset_cargos:
            self.cargoNormxEntry.setDoubleArray([])
            self.cargoNormyEntry.setDoubleArray([])
            self.cargoNormwEntry.setDoubleArray([])
            self.cargoIsRedEntry.setBooleanArray([])
