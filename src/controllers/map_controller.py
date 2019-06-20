import importlib
import typing

import cocos

from toolbox.singleton import Singleton
from views.map.events.move_event import MoveEvent
from views.map.map_scene import MapScene
from views.map.player_action_enum import PlayerActionEnum
from views.map.player_direction_enum import PlayerDirectionEnum
from views.map.player_layer import PlayerLayer


class MapController(metaclass=Singleton):
    """Manages the maps."""

    def load_map(self, map_file: str, players_position: typing.Tuple[int, int]):
        """Load the map file.

        :param: map_file: The path to the map file.
        :param: players_position: The tile coordinates of the player's position.
        """

        self._map = cocos.tiles.load(map_file)
        self._map_scene = MapScene(self, self._map, players_position)

    def action(self, position: typing.Tuple[int, int], direction: PlayerDirectionEnum, action: PlayerActionEnum,
               **kwargs) -> None:
        """Trigger the events after the player's action.

        :param position: The player's position on the map in pixels.
        :param direction: The direction the player is facing.
        :param action: The player's action.
        :param: args: The optional arguments depending on the action.
        """

        x = position[0] - self._map_scene.TILE_SIZE / 2
        y = position[1] - PlayerLayer.CHAR_HEIGHT / 2

        if action == PlayerActionEnum.PLAYER_WANT_MOVE:
            MoveEvent(self._map_scene, x, y, direction, kwargs["new_direction"], self._map)

        if action.name in self._map.contents:
            resource = self._map.get_resource(action.name)
            objects = resource.get_in_region(x - MapScene.TILE_SIZE,
                                             y - MapScene.TILE_SIZE,
                                             x + MapScene.TILE_SIZE * 2,
                                             y + MapScene.TILE_SIZE * 2)
            for object in objects:
                for property, value in object.properties.items():
                    class_name = property.replace("_", " ").title().replace(" ", "")
                    event_class = getattr(
                        importlib.import_module("views.map.events.{0}_event".format(property.lower())),
                        "{0}Event".format(class_name)
                    )

                    event_class(self._map_scene, x, y, direction, object)
