from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from toolbox.game import Game


class BattleModel:
    """The data representing a battle."""

    def __init__(self) -> None:
        """Create a new battle."""

        self._players_pokemon = self._first_players_pokemon_available(Game().game_state.player.pokemons)
        self._opponent_pokemon = PokemonModel(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 5,
                                              [LearnedMoveModel(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp,
                                                                moves["VINE_WHIP"].default_pp),
                                               LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp,
                                                                moves["GROWL"].default_pp)])

    def _first_players_pokemon_available(self, pokemons) -> PokemonModel:
        """Get the first pokemon of the list who can fight.
        
        :return: A ``PokemonModel``.
        """

        for pokemon in Game().game_state.player.pokemons:
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

    @property
    def opponent_pokemon(self) -> PokemonModel:
        """Get the opponent fighting pokemon."""

        return self._opponent_pokemon

    @opponent_pokemon.setter
    def opponent_pokemon(self, opponent_pokemon) -> None:
        """Set the opponent fighting pokemon.

        :param opponent_pokemon: The opponent fighting pokemon.
        """
