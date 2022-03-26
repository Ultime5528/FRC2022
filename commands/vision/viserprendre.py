import commands2

from commands.intake.prendreballon import PrendreBallon
from commands.vision.visercargo import ViserCargo
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets


class ViserPrendre(commands2.ParallelCommandGroup):
    def __init__(self, basepilotable: BasePilotable, intake: Intake, vision: VisionTargets):
        super().__init__(
            ViserCargo(basepilotable, vision),
            PrendreBallon(intake)
        )
