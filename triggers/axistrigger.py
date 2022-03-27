import commands2
import wpilib


class AxisTrigger(commands2.Trigger):
    def __init__(self, stick: wpilib.Joystick, axis: int, inverted: bool = False):
        super().__init__(lambda: stick.getRawAxis(axis) < -0.5 if inverted else stick.getRawAxis(axis) > 0.5)
