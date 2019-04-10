import typing

from models.pokemon_model import PokemonModel


class PlayerModel:
    """The player of the game."""

    def __init__(self) -> None:
        """Create a new player."""

        super().__init__()
        self._name = "John"
        self._pokemons = []

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

        for pokemon in self._pokemons:
            if pokemon.hp > 0:
                return True

        return False
