import typing

import cocos

from views.map.player_layer import PlayerLayer
from .player_direction_enum import PlayerDirectionEnum


class MapScene(cocos.scene.Scene):
    """The scene displaying a map on which the player can move.

    - PLAYER_LAYER_NAME: The name of the layer where the player's sprite must be added.
    """

    PLAYER_LAYER_NAME = "PLAYER"

    def __init__(self, map_controller, map: cocos.tiles.Resource, players_position: typing.Tuple[int, int]) -> None:
        """Create the map scene.

        Add all the layers of the map and the player.

        :param map_controller: The controller of the maps.
        :param: players_position: The tile coordinates of the player's position.
        """

        super().__init__()

        self._scroller = cocos.layer.ScrollingManager()

        for key, value in map.contents.items():
            if isinstance(value, cocos.tiles.RectMapLayer):
                self._scroller.add(value)
                if key == MapScene.PLAYER_LAYER_NAME:
                    break

        self._player_layer = PlayerLayer(map_controller, players_position)
        self._scroller.add(self._player_layer)
        self._scroller.set_focus(PlayerLayer.TILE_SIZE / 2 + players_position[0] * PlayerLayer.TILE_SIZE,
                                 PlayerLayer.CHAR_HEIGHT / 2 + players_position[1] * PlayerLayer.TILE_SIZE)

        has_passed_player_layer = False
        for key, value in map.contents.items():
            if has_passed_player_layer and isinstance(value, cocos.tiles.RectMapLayer):
                self._scroller.add(value)

            if key == MapScene.PLAYER_LAYER_NAME:
                has_passed_player_layer = True

        self.add(self._scroller)

        cocos.director.director.replace(self)

    def move_player(self, direction: PlayerDirectionEnum) -> None:
        """Move the player in the given direction.

        :param: direction: The direction of the movement.
        """

        self._player_layer.direction = direction
