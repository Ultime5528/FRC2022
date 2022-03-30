import commands2

import properties
from commands.basepilotable.avancer import Avancer
from commands.vision.visercargo import ViserCargo
from subsystems.basepilotable import BasePilotable
from subsystems.visiontargets import VisionTargets


class ViserCargoAvancer(commands2.SequentialCommandGroup):
    def __init__(self, base_pilotable: BasePilotable, vision_targets: VisionTargets):
        super().__init__(
            ViserCargo(base_pilotable, vision_targets),
            Avancer(
                base_pilotable,
                lambda: properties.values.viser_cargo_distance_supp,
                lambda: properties.values.viser_cargo_forward_speed,
            )
        )
        self.setName(self.__class__.__name__)