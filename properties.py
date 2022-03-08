from networktables.util import ntproperty
import types
import sys


class Properties:
    viser_hub_speed = ntproperty("Properties/viser_hub_speed", 0.1, writeDefault=False)
    viser_hub_threshold = ntproperty("Properties/viser_hub_threshold", 0.2, writeDefault=False)
    viser_hub_x_offset = ntproperty("Properties/viser_hub_x_offset", 0.05, writeDefault=False)

    shooter_backspin_speed = ntproperty("Properties/shooter_backspin_speed", 1, writeDefault=False)
    shooter_speed = ntproperty("Properties/shooter_speed", 1, writeDefault=False)

    intake_speed = ntproperty("Properties/intake_speed", 1, writeDefault=False)
    intake_duree_ejection = ntproperty("Properties/intake_duree_ejection", 1.5, writeDefault=False)
    intake_reverse_speed = ntproperty("Properties/intake_reverse_speed", -1, writeDefault=False)

    transporter_reverse_speed = ntproperty("Properties/transporter_reverse_speed", -1, writeDefault=False)
    transporter_speed = ntproperty("Properties/transporter_speed", 1, writeDefault=False)

    trajectoire_angle_p = ntproperty("Properties/trajectoire_angle_p", 0.008, writeDefault=False)
    trajectoire_vue_avant = ntproperty("Properties/trajectoire_vue_avant", 0.25, writeDefault=False)
    
    grimpeur_vitesse_monter = ntproperty("Properties/grimpeur_vitesse_monter", 0.5, writeDefault=False)
    grimpeur_vitesse_descend = ntproperty("Properties/grimpeur_vitesse_descend", -0.5, writeDefault=False)
    grimpeur_vitesse_monter_secondaire = ntproperty("Properties/grimpeur_vitesse_monter_secondaire", 0.5, writeDefault=False)
    grimpeur_vitesse_descend_secondaire = ntproperty("Properties/grimpeur_vitesse_descend_secondaire", -0.5, writeDefault=False)
    grimpeur_distance_alignement = ntproperty("Properties/grimpeur_distance_alignement", 1, writeDefault=False)

    viser_hub_speed = ntproperty("/Properties/viser_hub_speed", 0.3, writeDefault=False)
    viser_hub_threshold = ntproperty("/Properties/viser_hub_threshold", 0.05, writeDefault=False)
    viser_hub_x_offset = ntproperty("/Properties/viser_hub_x_offset", 0, writeDefault=False)
    viser_cargo_forward_speed = ntproperty("Properties/viser_cargo_forward_speed", 0.3, writeDefault=False)
    viser_cargo_turn_speed = ntproperty("Properties/viser_cargo_turn_speed", 0.3, writeDefault=False)
    viser_cargo_x_threshold = ntproperty("Properties/viser_cargo_x_threshold", 0.05, writeDefault=False)
    viser_cargo_y_threshold = ntproperty("Properties/viser_cargo_y_threshold", 0.05, writeDefault=False)
    viser_cargo_x_offset = ntproperty("Properties/viser_cargo_x_offset", 0.05, writeDefault=False)
    viser_cargo_y_offset = ntproperty("Properties/viser_cargo_y_offset", 0.05, writeDefault=False)



    ejecter_shooter_temps = 4

values = Properties()

