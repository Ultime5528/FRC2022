import commands2
import wpilib

import ports


class LEDController(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()
        self.led_strip = wpilib.AddressableLED(ports.led_strip)
        self.buffer = [wpilib.AddressableLED.LEDData() for _ in range(300)]
        self.led_strip.setLength(len(self.buffer))
        self.firstPixelHue = 0
        self.led_strip.start()

    def rainbow(self):
        for i in range(len(self.buffer)):
            pixel_hue = (self.firstPixelHue + int(i * 180 / len(self.buffer))) % 180
            self.buffer[i].setHSV(pixel_hue, 255, i)

        self.firstPixelHue += 3
        self.firstPixelHue %= 180

    def periodic(self) -> None:
        self.rainbow()
        self.led_strip.setData(self.buffer)
