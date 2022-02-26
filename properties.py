from networktables.util import ntproperty


class Properties:
    viser_hub_speed = ntproperty("Properties/ViserHubSpeed", 0.3, writeDefault=False)
    viser_hub_threshold = ntproperty("Properties/ViserHubThreshold", 0.05, writeDefault=False)
    viser_hub_x_offset = ntproperty("Properties/ViserHubXOffset", 0.05, writeDefault=False)
    
    grimpeur_vitesse_monter = ntproperty("Properties/VitesseGrimpeurmonter", 0.5, writeDefault=False)
    vitesse_grimpeur_descend = ntproperty("Properties/VitesseGrimpeurDescend", -0.5, writeDefault=False)
    grimpeur_vitesse_monter_secondaire = ntproperty("Properties/VitesseGrimpeurmonterSecondaire", 0.5, writeDefault=False)
    vitesse_grimpeur_descend_secondaire = ntproperty("Properties/VitesseGrimpeurDescendSecondaire", -0.5, writeDefault=False)

values = Properties()



