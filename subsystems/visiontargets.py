from networktables import NetworkTables


class VisionTargets:
    def __init__(self) -> None:
        self.normxEntry = NetworkTables.getEntry("Vision/Hub/Norm_X")
        self.normyEntry = NetworkTables.getEntry("Vision/Hub/Norm_Y")

    @property
    def normX(self):
        return self.normxEntry.getDouble(0)

    @property
    def normY(self):
        return self.normyEntry.getDouble(0)
