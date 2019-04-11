import typing
from enum import Enum

from .action_enum import ActionEnum


class PkmnInfosTypeEnum(Enum):
    """The list of types for the PKMN infos scene."""

    NORMAL = (0, [ActionEnum.PREVIOUS, ActionEnum.CANCEL, ActionEnum.NEXT], ActionEnum.CANCEL)
    SHIFT = (1, [ActionEnum.PREVIOUS, ActionEnum.SHIFT, ActionEnum.CANCEL, ActionEnum.NEXT], ActionEnum.CANCEL)
    SHIFT_POKEMON_OUT = (
        2, [ActionEnum.PREVIOUS, ActionEnum.SHIFT, ActionEnum.CANCEL, ActionEnum.NEXT], ActionEnum.CANCEL)
    NEW_MOVE = (3, [ActionEnum.MOVE_1, ActionEnum.MOVE_2, ActionEnum.MOVE_3, ActionEnum.MOVE_4, ActionEnum.NEW_MOVE],
                ActionEnum.NEW_MOVE)

    def __init__(self, id: int, actions: typing.List[ActionEnum], default_action: ActionEnum) -> None:
        """Create a new PKMN infos type.

        :param id: The unique identifier.
        :param actions: The list of displayed actions.
        :param default_action: The selected action by default.
        """

        super().__init__()

        self._id = id
        self._actions = actions
        self._default_action = default_action

    @property
    def id(self) -> int:
        """Get the unique identifier.

        :return: The identifier.
        """

        return self._id

    @property
    def actions(self) -> typing.List[ActionEnum]:
        """Get the list of actions.

        :return: The list of ``ActionEnum``.
        """

        return self._actions

    @property
    def default_action(self) -> ActionEnum:
        """Get the selected action by default.

        :return: The ``ActionEnum`` selected by default.
        """

        return self._default_action
