from networktables.util import ntproperty
import types
import sys

viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)


class Properties(types.ModuleType):
    shooter_speed = ntproperty("Properties/ShooterSpeed", 1, writeDefault=False)
    backspin_shooter_speed = ntproperty("Properties/BackspinShooterSpeed", 1, writeDefault=False)


sys.modules[__name__] = Properties(__name__)

