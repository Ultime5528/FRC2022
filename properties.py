from networktables.util import ntproperty

persistent = True


class Properties:
    shooter_backspin_speed = ntproperty("/Properties/shooter_backspin_speed", 100, writeDefault=False, persistent=persistent)
    shooter_speed = ntproperty("/Properties/shooter_speed", 100, writeDefault=False, persistent=persistent)

    shooter_ejecter_speed = ntproperty("/Properties/shooter_ejecter_speed", 2000, writeDefault=False, persistent=persistent)
    shooter_ejecter_backspin_speed = ntproperty("/Properties/shooter_ejecter_backspin_speed", 100, writeDefault=False, persistent=persistent)
    shooter_ejecter_temps = ntproperty("/Properties/shooter_ejecter_temps", 4, writeDefault=False, persistent=persistent)

    intake_speed = ntproperty("/Properties/intake_speed", 1, writeDefault=False, persistent=persistent)
    intake_duree_ejection = ntproperty("/Properties/intake_duree_ejection", 1.5, writeDefault=False, persistent=persistent)
    intake_reverse_speed = ntproperty("/Properties/intake_reverse_speed", -1, writeDefault=False, persistent=persistent)

    transporter_reverse_speed = ntproperty("/Properties/transporter_reverse_speed", -1, writeDefault=False, persistent=persistent)
    transporter_speed = ntproperty("/Properties/transporter_speed", 1, writeDefault=False, persistent=persistent)

    trajectoire_angle_p = ntproperty("/Properties/trajectoire_angle_p", 0.008, writeDefault=False, persistent=persistent)
    trajectoire_vue_avant = ntproperty("/Properties/trajectoire_vue_avant", 0.25, writeDefault=False, persistent=persistent)
    
    grimpeur_vitesse_monter = ntproperty("/Properties/grimpeur_vitesse_monter", 0.5, writeDefault=False, persistent=persistent)
    grimpeur_vitesse_descend = ntproperty("/Properties/grimpeur_vitesse_descend", -0.5, writeDefault=False, persistent=persistent)
    grimpeur_vitesse_monter_secondaire = ntproperty("/Properties/grimpeur_vitesse_monter_secondaire", 0.5, writeDefault=False, persistent=persistent)
    grimpeur_vitesse_descend_secondaire = ntproperty("/Properties/grimpeur_vitesse_descend_secondaire", -0.5, writeDefault=False, persistent=persistent)
    grimpeur_distance_alignement = ntproperty("/Properties/grimpeur_distance_alignement", 1, writeDefault=False, persistent=persistent)

    viser_hub_speed = ntproperty("/Properties/viser_hub_speed", 0.3, writeDefault=False, persistent=persistent)
    viser_hub_threshold = ntproperty("/Properties/viser_hub_threshold", 0.05, writeDefault=False, persistent=persistent)
    viser_hub_x_offset = ntproperty("/Properties/viser_hub_x_offset", 0, writeDefault=False, persistent=persistent)
    viser_cargo_forward_speed = ntproperty("/Properties/viser_cargo_forward_speed", 0.3, writeDefault=False, persistent=persistent)
    viser_cargo_turn_speed = ntproperty("/Properties/viser_cargo_turn_speed", 0.3, writeDefault=False, persistent=persistent)
    viser_cargo_x_threshold = ntproperty("/Properties/viser_cargo_x_threshold", 0.05, writeDefault=False, persistent=persistent)
    viser_cargo_y_threshold = ntproperty("/Properties/viser_cargo_y_threshold", 0.05, writeDefault=False, persistent=persistent)
    viser_cargo_x_offset = ntproperty("/Properties/viser_cargo_x_offset", 0.05, writeDefault=False, persistent=persistent)
    viser_cargo_y_offset = ntproperty("/Properties/viser_cargo_y_offset", 0.05, writeDefault=False, persistent=persistent)


values = Properties()

