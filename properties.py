from networktables.util import ntproperty


class Properties:
    viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.1, writeDefault=False)
    viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.2, writeDefault=False)
    viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)
    intake_speed = ntproperty("Properties/intake_speed", 1, writeDefault=False)
    transporter_speed = ntproperty("Properties/transporter_speed", 1, writeDefault=False)
    reverse_intake_speed = ntproperty("Properties/reverse_intake_speed", -1, writeDefault=False)
    reverse_transporter_speed = ntproperty("Properties/reverse_transporter_speed", -1, writeDefault=False)
    intake_duree_ejection = ntproperty("Properties/intake_duree_ejection", 1.5, writeDefault=False)
    trajectoire_angle_p = ntproperty("Properties/trajectoire_angle_p", 0.008, writeDefault=False)
    trajectoire_vue_avant = ntproperty("Properties/trajectoire_vue_avant", 0.25, writeDefault=False)
    
    grimpeur_vitesse_monter = ntproperty("Properties/VitesseGrimpeurMonter", 0.5, writeDefault=False)
    vitesse_grimpeur_descend = ntproperty("Properties/VitesseGrimpeurDescend", -0.5, writeDefault=False)
    grimpeur_vitesse_monter_secondaire = ntproperty("Properties/VitesseGrimpeurMonterSecondaire", 0.5, writeDefault=False)
    vitesse_grimpeur_descend_secondaire = ntproperty("Properties/VitesseGrimpeurDescendSecondaire", -0.5, writeDefault=False)
    viser_hub_speed = ntproperty("/Properties/ViserHubSpeed", 0.3, writeDefault=False)
    viser_hub_threshold = ntproperty("/Properties/ViserHubThreshold", 0.05, writeDefault=False)
    viser_hub_x_offset = ntproperty("/Properties/ViserHubXOffset", 0, writeDefault=False)
    viser_cargo_forward_speed = ntproperty("Properties/ViserCargoForwardSpeed", 0.3, writeDefault=False)
    viser_cargo_turn_speed = ntproperty("Properties/ViserCargoTurnSpeed", 0.3, writeDefault=False)
    viser_cargo_x_threshold = ntproperty("Properties/ViserCargoXThreshold", 0.05, writeDefault=False)
    viser_cargo_y_threshold = ntproperty("Properties/ViserCargoYThreshold", 0.05, writeDefault=False)
    viser_cargo_x_offset = ntproperty("Properties/ViserCargoXOffset", 0.05, writeDefault=False)
    viser_cargo_y_offset = ntproperty("Properties/ViserCargoYOffset", 0.05, writeDefault=False)
    backspin_shooter_speed = ntproperty("Properties/BackspinShooterSpeed", 1, writeDefault=False)
    shooter_speed = ntproperty("Properties/ShooterSpeed", 1, writeDefault=False)
    ejecter_ballon_temps = 4
    distance_alignement_grimpeur =ntproperty("Properties/DistanceAlignementGrimpeur", 1, writeDefault=False)
values = Properties()



