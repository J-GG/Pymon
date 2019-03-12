from models.game_state_model import GameStateModel
from models.settings.settings_model import SettingsModel
from toolbox.singleton import Singleton


class Game(metaclass=Singleton):
    """Keep track of the data of the game."""

    def __init__(self) -> None:
        """Create a new Game."""

        super().__init__()
        self._settings = SettingsModel.load()
        self._game_state = GameStateModel.load()

    @property
    def settings(self) -> SettingsModel:
        """Get the settings.

        :return: The ``SettingsModel``.
        """

        return self._settings

    @property
    def game_state(self) -> GameStateModel:
        """Get the same state.

        :return: The ``GameStateModel``.
        """

        return self._game_state

    @game_state.setter
    def game_state(self, game_state) -> None:
        """Set the game state.

        :param game_state: The ``GameStateModel``.
        """

        self._game_state = game_state
