import time
import typing

from models.persistence import Persistence
from models.player_model import PlayerModel
from toolbox.init import PATH


class GameStateModel(Persistence):
    """Contain all the data of the game."""

    FILE_NAME = "game_state"
    DEFAULT_MAP = PATH + "/assets/map/map.tmx"
    DEFAULT_PLAYERS_POSITION = (11, 11)

    def __init__(self) -> None:
        """Create a new game state."""

        super().__init__()
        self._player = PlayerModel()
        self._time = 0
        self._time_start = time.time()
        self._map = GameStateModel.DEFAULT_MAP
        self._map_players_position = GameStateModel.DEFAULT_PLAYERS_POSITION

    @property
    def player(self) -> PlayerModel:
        """Get the player.

        :return: The ``PlayerModel``.
        """
        return self._player

    @property
    def time(self) -> int:
        """Get the number of seconds played.

        :return: The number of seconds played.
        """

        return self._time

    @property
    def map(self) -> str:
        """Return the path to the current map file.

        :return: A String representing a path.
        """

        return self._map

    @map.setter
    def map(self, map: str) -> None:
        """Set the path to the current map file.

        :param map: A String representing a path.
        """

        self._map = map

    @property
    def map_players_position(self) -> typing.Tuple[int, int]:
        """Get the player's position on the current map.

        :return: The tile coordinates of the player's position.
        """

        return self._map_players_position

    @map_players_position.setter
    def map_players_position(self, map_players_position: typing.Tuple[int, int]) -> None:
        """Set the player's position on the current map.

        :param map_players_position: The tile coordinates of the player's position.
        """

        self._map_players_position = map_players_position

    def start_time(self) -> None:
        """Set the start time for the game session to the current time."""

        self._time_start = time.time()

    def save(self) -> None:
        """Save te model into a file.

        Update the time value by adding the difference between the current
        time and the start time to the time attribute.
        """

        self._time += time.time() - self._time_start

        super().save()
