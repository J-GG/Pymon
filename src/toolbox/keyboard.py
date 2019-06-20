from models.settings.controls_enum import ControlsEnum
from toolbox.game import Game


def is_key_up(key: int) -> bool:
    """Get whether the pressed key is ``ControlsEnum.UP``.

    :param key: The pressed key.
    :return: True if the pressed key is ``ControlsEnum.UP``.
    """

    return key == Game().settings.controls[ControlsEnum.UP]


def is_key_down(key: int) -> bool:
    """Get whether the pressed key is ``ControlsEnum.DOWN``.

    :param key: The pressed key.
    :return: True if the pressed key is ``ControlsEnum.DOWN``.
    """

    return key == Game().settings.controls[ControlsEnum.DOWN]


def is_key_left(key: int) -> bool:
    """Get whether the pressed key is ``ControlsEnum.LEFT``.

    :param key: The pressed key.
    :return: True if the pressed key is ``ControlsEnum.LEFT``.
    """
    return key == Game().settings.controls[ControlsEnum.LEFT]


def is_key_right(key: int) -> bool:
    """Get whether the pressed key is ``ControlsEnum.RIGHT``.

    :param key: The pressed key.
    :return: True if the pressed key is ``ControlsEnum.RIGHT``.
    """

    return key == Game().settings.controls[ControlsEnum.RIGHT]


def is_key_action(key: int) -> bool:
    """Get whether the pressed key is ``ControlsEnum.ACTION``.

    :param key: The pressed key.
    :return: True if the pressed key is ``ControlsEnum.ACTION``.
    """

    return key == Game().settings.controls[ControlsEnum.ACTION]


def is_key_cancel(key: int) -> bool:
    """Get whether the pressed key is ControlsEnum.CANCEL.

    :param key: The pressed key.
    :return: True if the pressed key is ControlsEnum.CANCEL.
    """

    return key == Game().settings.controls[ControlsEnum.CANCEL]
