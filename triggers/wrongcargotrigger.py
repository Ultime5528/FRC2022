import commands2

from subsystems.visiontargets import VisionTargets


class WrongCargoTrigger(commands2.Trigger):
    def __init__(self, visiontargets: VisionTargets):
        super().__init__(lambda: visiontargets.hasWrongCargoNear())
