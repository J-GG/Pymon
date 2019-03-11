import os
import typing

import dill

from models.game_state_model import GameStateModel
from .init import PATH


class Game:
    """Manages the persistence of the data."""

    GAME_STATE_PATH = PATH + "/data/game_state"
    if not os.path.exists(PATH + "/data"):
        os.makedirs(PATH + "/data")
        
    game_state = None

    @staticmethod
    def set_game_state(game_state: GameStateModel) -> None:
        Game.game_state = game_state

    @staticmethod
    def save() -> None:
        """Save the game state into a file."""

        Game.game_state.update_time()
        with open(Game.GAME_STATE_PATH, 'w+b') as game_state_file:
            dill.dump(Game.game_state, game_state_file)

    @staticmethod
    def load() -> typing.Union[None, GameStateModel]:
        """Load the game state file.

        :return The loaded game state.
        """

        if os.path.isfile(Game.GAME_STATE_PATH):
            with open(Game.GAME_STATE_PATH, "rb") as game_state_file:
                deserialized_game_state = dill.load(game_state_file)
                return deserialized_game_state
        else:
            return None

    @staticmethod
    def delete() -> None:
        """Remove the game state file."""

        os.remove(Game.GAME_STATE_PATH)
