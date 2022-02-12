from networktables.util import ntproperty

viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)
