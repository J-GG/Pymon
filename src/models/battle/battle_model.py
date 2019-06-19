import typing

from models.pokemon_model import PokemonModel
from toolbox.game import Game


class BattleModel:
    """The data representing a battle."""

    def __init__(self, opponent_pokemons: typing.List[PokemonModel], place: str) -> None:
        """Create a new battle.

        :param opponent_pokemons: The list of opponent fighting pokemon.
        :param place: The place where the battle takes place (i.e. the background).
        """

        self._players_pokemon = self._first_players_pokemon_available(Game().game_state.player.pokemons)
        self._opponent_pokemon = self._first_players_pokemon_available(opponent_pokemons)
        self._place = place

    def _first_players_pokemon_available(self, pokemons: typing.List[PokemonModel]) -> PokemonModel:
        """Get the first pokemon of the list who can fight.
        
        :return: A  list of ``PokemonModel``.
        """

        for pokemon in pokemons:
            if pokemon.hp > 0:
                return pokemon

    @property
    def players_pokemon(self) -> PokemonModel:
        """Get the player's fighting pokemon."""

        return self._players_pokemon

    @players_pokemon.setter
    def players_pokemon(self, players_pokemon) -> None:
        """Set the player's fighting pokemon.

        :param players_pokemon: The player's fighting pokemon.
        """
        self._players_pokemon = players_pokemon

    @property
    def opponent_pokemon(self) -> PokemonModel:
        """Get the opponent fighting pokemon."""

        return self._opponent_pokemon

    @opponent_pokemon.setter
    def opponent_pokemon(self, opponent_pokemon) -> None:
        """Set the opponent fighting pokemon.

        :param opponent_pokemon: The opponent fighting pokemon.
        """

        self._opponent_pokemon = opponent_pokemon

    @property
    def place(self) -> str:
        """Get the place where the battle takes place.

        :return: The place where the battle takes place.
        """

        return self._place

    def shift_players_pokemon(self, players_pokemon: PokemonModel) -> PokemonModel:
        """Shift the player's pokemon with the specified one and return the
        previously fighting pokemon.
        
        :param players_pokemon: The player's fighting pokemon.
        """

        previous_pokemon = self.players_pokemon
        self._players_pokemon = players_pokemon

        return previous_pokemon

    def is_wild_pokemon(self) -> bool:
        """Whether the battle is against a wild pokemon or not.

        :return True if the battle is against a wild pokemon.
        """

        return True
