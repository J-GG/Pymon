from enum import Enum

from pyglet.window import key


class ControlsEnum(Enum):
    """List of the controls for the game."""

    ACTION = key.ENTER
    CANCEL = key.B
    UP = key.UP
    DOWN = key.DOWN
    RIGHT = key.RIGHT
    LEFT = key.LEFT
