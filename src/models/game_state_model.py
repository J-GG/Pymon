import time

from models.persistence import Persistence
from models.player_model import PlayerModel


class GameStateModel(Persistence):
    """Contain all the data of the game."""

    FILE_NAME = "game_state"

    def __init__(self) -> None:
        """Create a new game state."""

        super().__init__()
        self._player = PlayerModel()
        self._time = 0
        self._time_start = time.time()

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
