import math

import wpilib
import commands2
import ports
import numpy as np

def interpoler(t, couleur1, couleur2):
    assert 0 <= t <= 1
    return (1 - t) * couleur1 + t * couleur2

class LEDController(commands2.SubsystemBase):
    red_hsv = np.array([0, 255, 255])
    blue_hsv = np.array([120, 255, 255])
    black = np.array([0, 0, 0])

    def __init__(self):
        super().__init__()
        self.led_strip = wpilib.AddressableLED(ports.led_strip)
        self.buffer = [wpilib.AddressableLED.LEDData() for _ in range(300)]
        self.led_strip.setLength(len(self.buffer))
        self.time = 0
        self.led_strip.start()

    def rainbow(self):
        for i in range(len(self.buffer)):
            pixel_hue = (self.time + int(i * 180 / len(self.buffer))) % 180
            self.buffer[i].setHSV(pixel_hue, 255, i)

        self.time += 3
        self.time %= 180

    def select_team(self):
        pixel_value = round(math.cos(self.time / (16 * math.pi)) * 255)
        for i in range(len(self.buffer)):
            if pixel_value >= 0:
                self.buffer[i].setHSV(125, 255, pixel_value)
            else:
                self.buffer[i].setHSV(0, 255, abs(pixel_value))
        self.time += 1


    def periodic(self) -> None:
        self.select_team()
        self.led_strip.setData(self.buffer)
