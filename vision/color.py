from enum import Enum


class Color(Enum):
    RED = "red_ball"
    BLUE = "blue_ball"

    @property
    def bgr(self):
        if self == Color.RED:
            return 0, 0, 255
        elif self == Color.BLUE:
            return 255, 0, 0
        else:
            raise NotImplementedError()
