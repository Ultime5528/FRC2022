from networktables.util import ntproperty


class Properties:
    viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
    viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
    viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)
    intake_speed = ntproperty("Properties/intake_speed", 1, writeDefault=False)
    transporter_speed = ntproperty("Properties/transporter_speed", 1, writeDefault=False)
    reverse_intake_speed = ntproperty("Properties/reverse_intake_speed", -1, writeDefault=False)
    reverse_transporter_speed = ntproperty("Properties/reverse_transporter_speed", -1, writeDefault=False)
    intake_duree_ejection = ntproperty("Properties/intake_duree_ejection", 1.5, writeDefault=False)


values = Properties()
