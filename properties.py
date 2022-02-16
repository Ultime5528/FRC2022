from networktables.util import ntproperty

viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)

viser_cargo_forward_speed = ntproperty("Properties/ViserCargoForwardSpeed", 0.3, writeDefault=False)
viser_cargo_turn_speed = ntproperty("Properties/ViserCargoTurnSpeed", 0.3, writeDefault=False)
viser_cargo_x_threshold = ntproperty("Properties/ViserCargoXThreshold", 0.05, writeDefault=False)
viser_cargo_y_threshold = ntproperty("Properties/ViserCargoYThreshold", 0.05, writeDefault=False)
viser_cargo_x_offset = ntproperty("Properties/ViserCargoXOffset", 0.05, writeDefault=False)
viser_cargo_y_offset = ntproperty("Properties/ViserCargoYOffset", 0.05, writeDefault=False)
