from networktables import NetworkTables


class VisionHub:
    def __init__(self) -> None:
        self.normxEntry = NetworkTables.getEntry("Vision/Norm_X")
        self.normyEntry = NetworkTables.getEntry("Vision/Norm_Y")

    @property
    def normX(self):
        return self.normxEntry.getDouble(0)

    @property
    def normY(self):
        return self.normyEntry.getDouble(0)
