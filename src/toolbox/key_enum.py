from enum import Enum


class KeyEnum(Enum):
    """An enumeration matching the key int value with their legible name.

    The int values are those given by the cocos key events.
    """
    
    UP = 65362
    DOWN = 65364
    ENTER = 65293
    B = 98
