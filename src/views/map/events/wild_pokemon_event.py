import json
import random

import cocos

from views.map.map_scene import MapScene
from views.map.player_direction_enum import PlayerDirectionEnum


class WildPokemonEvent:
    """Fight against a wild pokemon."""

    def __init__(self, map_scene: MapScene, x: int, y: int, direction: PlayerDirectionEnum,
                 object: cocos.tiles.TmxObject) -> None:
        """Create an event to fight against a wild pokemon.

        :param map_scene: The scene containing the map.
        :param x: The x coordinate of the player on the map.
        :param y: The y coordinate of the player on the map.
        :param direction: The direction the player is facing.
        :param object: The object containing all the info about the event.
        """

        wild_pokemon = dict()
        if object.px <= x and object.px + object.width >= x and object.py <= y and object.py + object.height >= y:
            wild_pokemon = json.loads(object.properties["wild_pokemon"])

        if wild_pokemon:
            if random.random() >= 0.8:
                print("Battle against {0}!".format(
                    random.choice([x for x in wild_pokemon for y in range(wild_pokemon[x])])
                ))
