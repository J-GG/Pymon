import json
import random
import typing

import cocos

from toolbox.singleton import Singleton
from views.map.map_scene import MapScene
from views.map.player_action_enum import PlayerActionEnum
from views.map.player_direction_enum import PlayerDirectionEnum


class MapController(metaclass=Singleton):
    """Manages the maps."""

    def load_map(self, map_file: str, players_position: typing.Tuple[int, int]):
        """Load the map file.

        :param: map_file: The path to the map file.
        :param: players_position: The tile coordinates of the player's position.
        """

        self._map = cocos.tiles.load(map_file)
        self._map_scene = MapScene(self, self._map, players_position)

    def action(self, x: int, y: int, direction: PlayerDirectionEnum, action: PlayerActionEnum, **kwargs) -> None:
        """Determine the reaction to adopt after the player's action.

        :param x: The x tiles coordinates.
        :param y: the y tiles coordinates.
        :param direction: The direction the player is facing.
        :param action: The player's action.
        :param: args: The optional arguments depending on the action.
        """

        if direction == PlayerDirectionEnum.UP:
            player_direction = cocos.tiles.RectMap.UP
        elif direction == PlayerDirectionEnum.DOWN:
            player_direction = cocos.tiles.RectMap.DOWN
        elif direction == PlayerDirectionEnum.RIGHT:
            player_direction = cocos.tiles.RectMap.RIGHT
        else:
            player_direction = cocos.tiles.RectMap.LEFT

        if action == PlayerActionEnum.PLAYER_END_MOVE:
            wild_pokemon = dict()
            for key, value in self._map.contents.items():
                if isinstance(value, cocos.tiles.TmxObjectLayer):
                    for object in value.objects:
                        if "wild_pokemon" in object.properties and object.px <= x and object.px + object.width >= x and object.py <= y and object.py + object.height >= y:
                            wild_pokemon = json.loads(object.properties["wild_pokemon"])

            if wild_pokemon:
                if random.random() >= 0.8:
                    print("Battle against {0}!".format(
                        random.choice([x for x in wild_pokemon for y in range(wild_pokemon[x])])
                    ))
        elif action == PlayerActionEnum.PLAYER_START_MOVE:
            if kwargs["new_direction"] != direction:
                move = True
            else:
                walkable = True
                for key, value in self._map.contents.items():
                    if isinstance(value, cocos.tiles.RectMapLayer):
                        cell = value.get_neighbor(value.get_at_pixel(x, y), player_direction)
                        if not cell:
                            walkable = False
                            break
                        if cell.tile:
                            tile = cell.tile
                            if "walkable" not in tile.properties or tile.properties["walkable"] in (
                                    "false", "False", None):
                                walkable = False
                move = walkable

            if move:
                self._map_scene.move_player(kwargs["new_direction"])
        elif action == PlayerActionEnum.ACTION_BUTTON:
            for key, value in self._map.contents.items():
                if isinstance(value, cocos.tiles.TmxObjectLayer):
                    for object in value.objects:
                        if "message" in object.properties and object.px <= x and object.px + object.width >= x and object.py <= y and object.py + object.height >= y:
                            print(object.properties["message"])
