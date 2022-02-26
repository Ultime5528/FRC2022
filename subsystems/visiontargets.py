from networktables import NetworkTables


class VisionTargets:
    def __init__(self) -> None:
        self._normxEntry = NetworkTables.getEntry("Vision/Hub/_Norm_X")
        self._normyEntry = NetworkTables.getEntry("Vision/Hub/_Norm_Y")

    @property
    def normX(self):
        return self._normxEntry.getDouble(0)

    @property
    def normY(self):
        return self._normyEntry.getDouble(0)
