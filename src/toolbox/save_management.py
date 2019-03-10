import os
import typing

import dill

from models.pokemon_model import PokemonModel
from .init import PATH

_GAME_STATE_PATH = PATH + "/data/game_state.txt"


def save(players_pokemon) -> None:
    """Save the game state into a file.

    :param players_pokemon: The player's pokemon.
    """

    players_pokemon.heal()
    with open(_GAME_STATE_PATH, 'w+b') as game_state_file:
        dill.dump(players_pokemon, game_state_file)


def load() -> typing.Union[None, PokemonModel]:
    """Load the game state file.

    :return The load pokemon.
    """

    if os.path.isfile(_GAME_STATE_PATH):
        with open(_GAME_STATE_PATH, "rb") as game_state_file:
            deserialized_game_state = dill.load(game_state_file)
            return deserialized_game_state
    else:
        return None


def delete() -> None:
    """Remove the game state file."""

    os.remove(_GAME_STATE_PATH)
