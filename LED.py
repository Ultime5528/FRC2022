import random
from enum import Enum
import math
from typing import Callable, Union, Tuple, List

import wpilib
import commands2
import ports
import numpy as np

from subsystems.intake import Intake


def interpoler(t, couleur1, couleur2):
    assert 0 <= t <= 1
    return ((1 - t) * couleur1 + t * couleur2).astype(int)


Color = Union[np.ndarray, Tuple[int, int, int], List[int]]


class ModeLED(Enum):
    STARTUP = "startup"
    SHOOT = "shoot"


class LEDController(commands2.SubsystemBase):
    red_hsv = np.array([0, 255, 255])
    blue_hsv = np.array([120, 255, 255])
    black = np.array([0, 0, 0])
    white = np.array([0, 0, 255])

    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake

        self.led_strip = wpilib.AddressableLED(ports.led_strip)
        self.buffer = [wpilib.AddressableLED.LEDData() for _ in range(300)]
        self.led_strip.setLength(len(self.buffer))
        self.time = 0
        self.led_strip.start()

    def set_hsv(self, i: int, color: Color):
        self.buffer[i].setHSV(*color)

    def set_all(self, color_func: Callable[[int], Color]):
        for i in range(len(self.buffer)):
            self.set_hsv(i, color_func(i))

    def rainbow(self):
        for i in range(len(self.buffer)):
            pixel_hue = (self.time + int(i * 180 / len(self.buffer))) % 180
            self.buffer[i].setHSV(pixel_hue, 255, i)

        self.time += 3
        self.time %= 180

    def select_team(self):
        pixel_value = round(510 * math.cos((1 / (12 * math.pi)) * self.time))
        if pixel_value >= 0:
            color = (125, 255, pixel_value)
        else:
            color = (0, 255, abs(pixel_value))
        self.set_all(lambda i: color)

    def ripples(self, color):
        if self.time % 10 == 0:
            def get_color():
                if random.random() <= (1 - (wpilib.DriverStation.getMatchTime() / 15)):
                    return color
                else:
                    return self.white
            self.set_all(get_color)

    def waves(self, color, nombreballons):
        def get_color(i: int):
            prop = 0.5 * math.cos(2 * math.pi / (20/(nombreballons+1)) * (self.time / 5 + i)) + 0.5
            return interpoler(prop, color, self.black)
        self.set_all(get_color)

    def periodic(self) -> None:
        self.time += 1

        alliance = wpilib.DriverStation.getAlliance()
        if alliance == wpilib.DriverStation.Alliance.kInvalid:
            color = self.black
        elif alliance == wpilib.DriverStation.Alliance.kRed:
            color = self.red_hsv
        else:  # kBlue
            color = self.blue_hsv

        if wpilib.DriverStation.isAutonomous():
            self.ripples(color)
        elif wpilib.DriverStation.isTeleop():
            self.waves(color, self.intake.ballCount())
        else:  # game hasn't started
            if alliance == wpilib.DriverStation.Alliance.kInvalid:
                self.select_team()
            else:  # kBlue
                self.set_all(lambda i: color)

        self.led_strip.setData(self.buffer)
