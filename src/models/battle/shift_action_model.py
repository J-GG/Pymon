from models.battle.battle_model import BattleModel
from models.pokemon_model import PokemonModel


class ShiftActionModel:
    """Represents the shift of a pokemon by another."""

    def __init__(self, pokemon: PokemonModel) -> None:
        """Create a new shift action.

        :param pokemon: The ``PokemonModel`` being replaced.
        """

        self._pokemon = pokemon
        self._previous_pokemon = None

    def shift(self, battle: BattleModel) -> None:
        """Switch the pokemon.

        :param battle: The model containing the data of the battle.
        """

        self._previous_pokemon = battle.shift_players_pokemon(self._pokemon)

    @property
    def pokemon(self) -> PokemonModel:
        """Get the pokemon sent into battle.

        :return: The new fighting ``PokemonModel``.
        """

        return self._pokemon

    @property
    def previous_pokemon(self) -> PokemonModel:
        """Get the pokemon removed from the battle.

        :return The previously fighting ``PokemonModel``.
        """

        return self._previous_pokemon
