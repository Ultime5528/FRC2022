from typing import Union, Callable

FloatProperty = Union[float, Callable[[], float]]


def to_callable(val: FloatProperty) -> Callable[[], float]:
    if callable(val):
        return val
    return lambda: val
