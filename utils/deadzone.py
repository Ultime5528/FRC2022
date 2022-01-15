import math


def linear_deadzone(value, deadzone):
    scale_param = 1.0 - deadzone

    abs_value = abs(value)
    if abs_value < deadzone:
        return 0.0
    else:
        return math.copysign(
            (abs_value - deadzone) / scale_param, value
        )
