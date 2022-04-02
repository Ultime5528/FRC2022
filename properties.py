from networktables.util import ntproperty

persistent = True

# if not persistent:
#     raise NotImplementedError()
#     import os
#     for p in ["networktables.ini", "networktables.ini.bak"]:
#         if os.path.exists(p):
#
#             os.remove(p)


class Properties:
    aide_pilotage_slow_factor = ntproperty("/Properties/aide_pilotage_slow_factor", 0.5, writeDefault=False, persistent=persistent)

    shooter_backspin_speed = ntproperty("/Properties/shooter_backspin_speed", 1500, writeDefault=False, persistent=persistent)
    shooter_speed = ntproperty("/Properties/shooter_speed", 1500, writeDefault=False, persistent=persistent)

    shooter_ejecter_speed = ntproperty("/Properties/shooter_ejecter_speed", 1000, writeDefault=False, persistent=persistent)
    shooter_ejecter_backspin_speed = ntproperty("/Properties/shooter_ejecter_backspin_speed", 1000, writeDefault=False, persistent=persistent)
    shooter_ejecter_temps = ntproperty("/Properties/shooter_ejecter_temps", 2, writeDefault=False, persistent=persistent)
    shooter_feedforward_percentage = ntproperty("/Properties/shooter_feedforward_percentage", 0.95, writeDefault=False, persistent=persistent)
    shooter_tolerance = ntproperty("/Properties/shooter_tolerance", 100, writeDefault=False, persistent=persistent)
    shooter_end_time = ntproperty("/Properties/shooter_end_time", 4, writeDefault=False, persistent=persistent)

    intake_speed = ntproperty("/Properties/intake_speed", 0.4, writeDefault=False, persistent=persistent)
    intake_reverse_speed = ntproperty("/Properties/intake_reverse_speed", -0.5, writeDefault=False, persistent=persistent)
    intake_convoyeur_speed_lent = ntproperty("/Properties/intake_convoyeur_speed_lent", 0.44, writeDefault=False, persistent=persistent)
    intake_convoyeur_speed_rapide = ntproperty("/Properties/intake_convoyeur_speed_rapide", 0.6, writeDefault=False, persistent=persistent)
    intake_ultrason_bas_threshold = ntproperty("/Properties/intake_ultrason_bas_threshold", 0.25, writeDefault=False, persistent=persistent)
    intake_ultrason_haut_threshold = ntproperty("/Properties/intake_ultrason_haut_threshold", 0.6, writeDefault=False, persistent=persistent)

    trajectoire_angle_p = ntproperty("/Properties/trajectoire_angle_p", 0.016, writeDefault=False, persistent=persistent)
    trajectoire_vue_avant = ntproperty("/Properties/trajectoire_vue_avant", 0.1, writeDefault=False, persistent=persistent)

    grimpeur_primaire_vitesse_descendre = ntproperty("/Properties/grimpeur_primaire_vitesse_descendre", -0.5, writeDefault=False, persistent=persistent)
    grimpeur_primaire_vitesse_monter = ntproperty("/Properties/grimpeur_primaire_vitesse_monter", 0.5, writeDefault=False, persistent=persistent)
    grimpeur_primaire_vitesse_descendre_slow = ntproperty("/Properties/grimpeur_primaire_vitesse_descendre_slow", -0.25, writeDefault=False, persistent=persistent)
    grimpeur_primaire_start_speed = ntproperty("/Properties/grimpeur_primaire_start_speed", 0.2, writeDefault=False, persistent=persistent)
    grimpeur_primaire_end_speed = ntproperty("/Properties/grimpeur_primaire_end_speed", 1.0, writeDefault=False, persistent=persistent)
    grimpeur_primaire_accel = ntproperty("/Properties/grimpeur_primaire_accel", 0.03, writeDefault=False, persistent=persistent)
    grimpeur_primaire_hauteur_clip = ntproperty("/Properties/grimpeur_primaire_hauteur_clip", 245, writeDefault=False, persistent=persistent)
    grimpeur_primaire_hauteur_max = ntproperty("/Properties/grimpeur_primaire_hauteur_max", 275, writeDefault=False, persistent=persistent)

    grimpeur_secondaire_vitesse_descendre = ntproperty("/Properties/grimpeur_secondaire_vitesse_descendre", -0.75, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_vitesse_monter = ntproperty("/Properties/grimpeur_secondaire_vitesse_monter", 0.75, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_start_speed = ntproperty("/Properties/grimpeur_secondaire_start_speed", 0.2, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_end_speed = ntproperty("/Properties/grimpeur_secondaire_end_speed", 1.0, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_accel = ntproperty("/Properties/grimpeur_secondaire_accel", 0.03, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_hauteur_max = ntproperty("/Properties/grimpeur_secondaire_hauteur_max", 120, writeDefault=False, persistent=persistent)
    grimpeur_primaire_hauteur_level_3 = ntproperty("/Properties/grimpeur_primaire_hauteur_level_3", 50, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_hauteur_alignement_bas = ntproperty("/Properties/grimpeur_secondaire_hauteur_alignement_bas", 90.0, writeDefault=False, persistent=persistent)
    grimpeur_secondaire_hauteur_alignement_haut = ntproperty("/Properties/grimpeur_secondaire_hauteur_alignement_haut", 80.0,writeDefault=False, persistent=persistent)
    grimpeur_secondaire_hauteur_intake_haut = ntproperty("/properties/grimpeur_secondaire_hauteur_intake_haut", 10,writeDefault=False, persistent=persistent)

    vision_hub_rectangularity_threshold = ntproperty("/Properties/vision_hub_rectangularity_threshold", 0.5, writeDefault=False,persistent=persistent)
    vision_hub_perimeter_threshold = ntproperty("/Properties/vision_hub_perimeter_threshold", 7, writeDefault=False,persistent=persistent)
    vision_hub_maxErrorX_multiplier = ntproperty("/Properties/vision_hub_maxErrorX_multiplier", 0.4, writeDefault=False,persistent=persistent)
    vision_hub_maxErrorY_multiplier = ntproperty("/Properties/vision_hub_maxErrorY_multiplier", 0.2, writeDefault=False,persistent=persistent)

    vision_cargo_normw_threshold = ntproperty("/Properties/vision_cargo_normw_threshold", 0.4, writeDefault=False, persistent=persistent)
    vision_cargo_normy_threshold = ntproperty("/Properties/vision_cargo_normy_threshold", -0.5, writeDefault=False, persistent=persistent)
    vision_cargo_crop_x_min = ntproperty("/Properties/vision_cargo_crop_x_min", 0.11, writeDefault=False, persistent=persistent)
    vision_cargo_crop_x_max = ntproperty("/Properties/vision_cargo_crop_x_max", 0.85, writeDefault=False, persistent=persistent)
    vision_cargo_crop_y_min = ntproperty("/Properties/vision_cargo_crop_y_min", 0.4, writeDefault=False, persistent=persistent)
    vision_cargo_crop_y_max = ntproperty("/Properties/vision_cargo_crop_y_max", 0.78, writeDefault=False, persistent=persistent)
    vision_cargo_red_hsv_low = ntproperty("/Properties/vision_cargo_red_hsv_low", [165, 100, 70], writeDefault=False, persistent=persistent)
    vision_cargo_red_hsv_high = ntproperty("/Properties/vision_cargo_red_hsv_high", [7, 255, 255], writeDefault=False, persistent=persistent)
    vision_cargo_blue_hsv_low = ntproperty("/Properties/vision_cargo_blue_hsv_low", [87, 90, 50], writeDefault=False, persistent=persistent)
    vision_cargo_blue_hsv_high = ntproperty("/Properties/vision_cargo_blue_hsv_high", [115, 255, 255], writeDefault=False, persistent=persistent)
    vision_cargo_min_radius = ntproperty("/Properties/vision_cargo_min_radius", 0.03, writeDefault=False, persistent=persistent)
    vision_cargo_circularity_error = ntproperty("/Properties/vision_cargo_circularity_error", 0.2, writeDefault=False, persistent=persistent)

    viser_hub_speed = ntproperty("/Properties/viser_hub_speed", 0.085, writeDefault=False, persistent=persistent)
    viser_hub_threshold = ntproperty("/Properties/viser_hub_threshold", 0.04, writeDefault=False, persistent=persistent)
    viser_hub_x_offset = ntproperty("/Properties/viser_hub_x_offset", 0, writeDefault=False, persistent=persistent)

    viser_cargo_forward_speed = ntproperty("/Properties/viser_cargo_forward_speed", 0.2, writeDefault=False, persistent=persistent)
    viser_cargo_turn_speed = ntproperty("/Properties/viser_cargo_turn_speed", 1.0, writeDefault=False, persistent=persistent)
    viser_cargo_distance_supp = ntproperty("/Properties/viser_cargo_distance_supp", 0.5, writeDefault=False, persistent=persistent)
    viser_cargo_x_threshold = ntproperty("/Properties/viser_cargo_x_threshold", 0.1, writeDefault=False, persistent=persistent)
    viser_cargo_y_threshold = ntproperty("/Properties/viser_cargo_y_threshold", 0.1, writeDefault=False, persistent=persistent)
    viser_cargo_x_offset = ntproperty("/Properties/viser_cargo_x_offset", 0, writeDefault=False, persistent=persistent)
    viser_cargo_y_offset = ntproperty("/Properties/viser_cargo_y_offset", 0.05, writeDefault=False, persistent=persistent)


values = Properties()
