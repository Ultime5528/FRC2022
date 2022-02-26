from networktables.util import ntproperty
import types
import sys


class Properties:
    viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
    viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
    viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)
    intake_speed = ntproperty("Properties/intake_speed", 1, writeDefault=False)
    transporter_speed = ntproperty("Properties/transporter_speed", 1, writeDefault=False)
    reverse_intake_speed = ntproperty("Properties/reverse_intake_speed", -1, writeDefault=False)
    reverse_transporter_speed = ntproperty("Properties/reverse_transporter_speed", -1, writeDefault=False)
    intake_duree_ejection = ntproperty("Properties/intake_duree_ejection", 1.5, writeDefault=False)
    trajectoire_angle_p = ntproperty("Properties/trajectoire_angle_p", 0.008, writeDefault=False)
    trajectoire_vue_avant = ntproperty("Properties/trajectoire_vue_avant", 0.25, writeDefault=False)
    
    grimpeur_vitesse_monter = ntproperty("Properties/VitesseGrimpeurmonter", 0.5, writeDefault=False)
    vitesse_grimpeur_descend = ntproperty("Properties/VitesseGrimpeurDescend", -0.5, writeDefault=False)
    grimpeur_vitesse_monter_secondaire = ntproperty("Properties/VitesseGrimpeurmonterSecondaire", 0.5, writeDefault=False)
    vitesse_grimpeur_descend_secondaire = ntproperty("Properties/VitesseGrimpeurDescendSecondaire", -0.5, writeDefault=False)
    backspin_shooter_speed = ntproperty("Properties/BackspinShooterSpeed", 1, writeDefault=False)
    shooter_speed = ntproperty("Properties/ShooterSpeed", 1, writeDefault=False)
    ejecter_shooter_speed = ntproperty("Properties/EjecterShooterSpeed", 1, writeDefault=False)
    ejecter_backspin_shooter_speed = ntproperty("Properties/BackspinShooterSpeed", 1, writeDefault=False)
    ejecter_shooter_temps = ntproperty("Properties/EjecterShooterTemps", 4, writeDefault=False)

values = Properties()



