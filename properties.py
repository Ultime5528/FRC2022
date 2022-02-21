from networktables.util import ntproperty
import types
import sys



class Properties:
    viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
    viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
    viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)
    backspin_shooter_speed = ntproperty("Properties/BackspinShooterSpeed", 1, writeDefault=False
    shooter_speed = ntproperty("Properties/ShooterSpeed", 1, writeDefault=False)
values = Properties()
