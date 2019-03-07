import random

from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel


class RunActionModel:
    """Represents the attempt to run from a battle."""

    def __init__(self, pokemon: PokemonModel, opponent_pokemon: PokemonModel) -> None:
        """

        :param pokemon: The pokemon trying to escape.
        :param opponent_pokemon: The other pokemon.
        """

        self._pokemon = pokemon
        self._opponent_pokemon = opponent_pokemon
        self._is_run_successful = None

    def is_run_successful(self) -> None:
        """Determine whether the pokemon succeed in escaping from the battle.

        :return True if the pokemon escapes.
        """

        if self._is_run_successful is None:
            F = ((self._pokemon.stats[StatEnum.SPEED] * 128) / self._opponent_pokemon.stats[
                StatEnum.SPEED] + 30) % 256

            self._is_run_successful = F > random.randint(0, 255)

        return self._is_run_successful
