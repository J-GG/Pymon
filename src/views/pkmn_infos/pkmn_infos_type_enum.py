from enum import Enum

from .action_enum import ActionEnum


class PkmnInfosTypeEnum(Enum):
    """The list of types for the PKMN infos scene."""

    NORMAL = [ActionEnum.PREVIOUS, ActionEnum.CANCEL, ActionEnum.NEXT]
    SHIFT = [ActionEnum.PREVIOUS, ActionEnum.SHIFT, ActionEnum.CANCEL, ActionEnum.NEXT]
    NEW_MOVE = [ActionEnum.MOVE_1, ActionEnum.MOVE_2, ActionEnum.MOVE_3, ActionEnum.MOVE_4]
