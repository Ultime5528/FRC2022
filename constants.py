from networktables.util import ntproperty

class Ports:
    basepilotable_left = 1
    basepilotable_right = 2


class Properties:
    viser_speed = ntproperty("Properties/ViserSpeed", 0.3, writeDefault=False)
    viser_offset = ntproperty("Properties/ViserOffset", 0.05, writeDefault=False)