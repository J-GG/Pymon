import typing

from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons


class PlayerModel:
    """The player of the game."""

    def __init__(self) -> None:
        """Create a new player."""

        super().__init__()
        self._name = "John"
        self._pokemons = []
        self._pokemons.append(PokemonModel(pokemons["PIKACHU"], pokemons["PIKACHU"].name, 50, [
            LearnedMoveModel(moves["TAIL_WHIP"], moves["TAIL_WHIP"].default_pp, moves["TAIL_WHIP"].default_pp),
            LearnedMoveModel(moves["THUNDER_SHOCK"], moves["THUNDER_SHOCK"].default_pp,
                             moves["THUNDER_SHOCK"].default_pp),
            LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp),
        ]))
        self._pokemons.append(PokemonModel(pokemons["BULBASAUR"], pokemons["BULBASAUR"].name, 5, [
            LearnedMoveModel(moves["TACKLE"], moves["TACKLE"].default_pp, moves["TACKLE"].default_pp),
            LearnedMoveModel(moves["GROWL"], moves["GROWL"].default_pp, moves["GROWL"].default_pp),
            LearnedMoveModel(moves["VINE_WHIP"], moves["VINE_WHIP"].default_pp, moves["VINE_WHIP"].default_pp),
        ]))

    @property
    def name(self) -> str:
        """Get the name of the player.

        :return: The name of the player.
        """
        return self._name

    @name.setter
    def name(self, name):
        """Set the name of the player.

        :param name: The name of the player.
        """

        self._name = name

    @property
    def pokemons(self) -> typing.List[PokemonModel]:
        """Get the list of pokemons owned by the player.

        :return: The list of ``PokemonModel`` owned by the player.
        """

        return self._pokemons

    @pokemons.setter
    def pokemons(self, pokemons) -> None:
        """Set the list of pokemons owned by the player.

        :param pokemons: The list of ``PokemonModel`` owned by the player.
        """

    def has_conscious_pokemon(self) -> bool:
        """Get whether the player has still at least one pokemon with more than
        0 HP.

        :return: True if the player has still conscious pokemon.
        """

        for pokemon in pokemons:
            if pokemon.hp > 0:
                return True

        return False
