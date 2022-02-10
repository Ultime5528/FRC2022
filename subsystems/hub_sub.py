import commands2
from networktables import NetworkTables


class Hub_sub(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        self.normxEntry = NetworkTables.getEntry("Vision/nt_normx")
        self.normyEntry = NetworkTables.getEntry("Vision/nt_normy")

    @property
    def normX(self):
        return self.normxEntry.getDouble()

    @property
    def normY(self):
        return self.normyEntry.getDouble()