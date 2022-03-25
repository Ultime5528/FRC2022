from networktables.util import ntproperty

persistent = True


class Properties:
    shooter_backspin_speed = ntproperty("/Properties/shooter_backspin_speed", 100, writeDefault=False, persistent=persistent)
    shooter_speed = ntproperty("/Properties/shooter_speed", 100, writeDefault=False, persistent=persistent)

    shooter_ejecter_speed = ntproperty("/Properties/shooter_ejecter_speed", 750, writeDefault=False, persistent=persistent)
    shooter_ejecter_backspin_speed = ntproperty("/Properties/shooter_ejecter_backspin_speed", 750, writeDefault=False, persistent=persistent)
    shooter_ejecter_temps = ntproperty("/Properties/shooter_ejecter_temps", 2, writeDefault=False, persistent=persistent)
    shooter_feedforward_percentage = ntproperty("/Properties/shooter_feedforward_percentage", 0.95, writeDefault=False, persistent=persistent)
    shooter_tolerance = ntproperty("/Properties/shooter_tolerance", 100, writeDefault=False, persistent=persistent)
    shooter_end_time = ntproperty("/Properties/shooter_end_time", 4, writeDefault=False, persistent=persistent)

    intake_speed = ntproperty("/Properties/intake_speed", 1, writeDefault=False, persistent=persistent)
    intake_duree_ejection = ntproperty("/Properties/intake_duree_ejection", 1.5, writeDefault=False, persistent=persistent)
    intake_reverse_speed = ntproperty("/Properties/intake_reverse_speed", -1, writeDefault=False, persistent=persistent)

    transporter_reverse_speed = ntproperty("/Properties/transporter_reverse_speed", -1, writeDefault=False, persistent=persistent)
    transporter_speed = ntproperty("/Properties/transporter_speed", 1, writeDefault=False, persistent=persistent)
    intake_ultrason_bas_threshold = ntproperty("/Properties/intake_ultrason_bas_threshold", 0.5, writeDefault=False, persistent=persistent)
    intake_ultrason_haut_threshold = ntproperty("/Properties/intake_ultrason_haut_threshold", 0.5, writeDefault=False, persistent=persistent)

    trajectoire_angle_p = ntproperty("/Properties/trajectoire_angle_p", 0.008, writeDefault=False, persistent=persistent)
    trajectoire_vue_avant = ntproperty("/Properties/trajectoire_vue_avant", 0.25, writeDefault=False, persistent=persistent)
    
    grimpeur_vitesse_monter = ntproperty("/Properties/grimpeur_vitesse_monter", 0.5, writeDefault=False, persistent=persistent)
    grimpeur_vitesse_descend = ntproperty("/Properties/grimpeur_vitesse_descend", -0.5, writeDefault=False, persistent=persistent)
    grimpeur_vitesse_monter_secondaire = ntproperty("/Properties/grimpeur_vitesse_monter_secondaire", 0.25, writeDefault=False, persistent=persistent)
    grimpeur_vitesse_descend_secondaire = ntproperty("/Properties/grimpeur_vitesse_descend_secondaire", -0.25, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_hauteur_alignement = ntproperty("/Properties/grimpeur_secondaire_hauteur_alignement", 40, writeDefault=False, persistent=persistent)
    grimpeur_primaire_hauteur_max = ntproperty("/Properties/grimpeur_primaire_hauteur_max", 10, writeDefault=False)
    grimpeur_primaire_hauteur_clip = ntproperty("/Properties/grimpeur_primaire_hauteur_clip", 10, writeDefault=False)


    vision_cargo_normw_threshold = ntproperty("/Properties/vision_cargo_normw_threshold", 0.4, writeDefault=False, persistent=persistent)
    viser_hub_speed = ntproperty("/Properties/viser_hub_speed", 0.3, writeDefault=False, persistent=persistent)
    viser_hub_threshold = ntproperty("/Properties/viser_hub_threshold", 0.05, writeDefault=False, persistent=persistent)
    viser_hub_x_offset = ntproperty("/Properties/viser_hub_x_offset", 0, writeDefault=False, persistent=persistent)
    viser_cargo_forward_speed = ntproperty("/Properties/viser_cargo_forward_speed", 0.3, writeDefault=False, persistent=persistent)
    viser_cargo_turn_speed = ntproperty("/Properties/viser_cargo_turn_speed", 0.3, writeDefault=False, persistent=persistent)
    viser_cargo_x_threshold = ntproperty("/Properties/viser_cargo_x_threshold", 0.05, writeDefault=False, persistent=persistent)
    viser_cargo_y_threshold = ntproperty("/Properties/viser_cargo_y_threshold", 0.05, writeDefault=False, persistent=persistent)
    viser_cargo_x_offset = ntproperty("/Properties/viser_cargo_x_offset", 0, writeDefault=False, persistent=persistent)
    viser_cargo_y_offset = ntproperty("/Properties/viser_cargo_y_offset", 0, writeDefault=False, persistent=persistent)


values = Properties()

