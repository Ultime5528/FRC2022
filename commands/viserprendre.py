import commands2
from wpilib import Joystick

from commands.piloter import Piloter
from commands.prendreballon import PrendreBallon
from commands.visercargo import ViserCargo
from subsystems.basepilotable import BasePilotable
from subsystems.intake import Intake
from subsystems.visiontargets import VisionTargets


class ViserPrendre(commands2.ParallelCommandGroup):
    def __init__(self, basepilotable: BasePilotable, intake: Intake, vision: VisionTargets):
        super().__init__(
            ViserCargo(basepilotable, vision),
            PrendreBallon(intake)
        )
