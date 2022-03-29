import commands2

from commands.intake.prendreballon import PrendreBallon
from commands.vision.visercargoavancer import ViserCargoAvancer
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets


class ViserPrendre(commands2.ParallelCommandGroup):
    def __init__(self, basepilotable: BasePilotable, intake: Intake, vision: VisionTargets):
        super().__init__(
            ViserCargoAvancer(basepilotable, vision),
            PrendreBallon(intake)
        )
