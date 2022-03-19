import commands2

from subsystems.visiontargets import VisionTargets


class WrongCargoTrigger(commands2.Trigger):
    def __init__(self, visiontargets: VisionTargets):
        super(WrongCargoTrigger, self).__init__(self._get)
        self.visiontargets = visiontargets

    def _get(self):
        return self.visiontargets.wrongCargoNear()