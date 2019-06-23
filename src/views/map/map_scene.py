import typing

import cocos
import pyglet
from cocos.actions import Delay, CallFunc

from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.dialog import Dialog
from views.map.player_layer import PlayerLayer
from .player_direction_enum import PlayerDirectionEnum


class MapScene(cocos.scene.Scene):
    """The scene displaying a map on which the player can move.

    - PLAYER_LAYER_NAME: The name of the layer where the player's sprite must be added.
    - TILE_SIZE: The width and height of a tile in pixels.
    """

    PLAYER_LAYER_NAME = "PLAYER"
    TILE_SIZE = 16

    def __init__(self, map_controller, map: cocos.tiles.Resource, players_position: typing.Tuple[int, int]) -> None:
        """Create the map scene.

        Add all the layers of the map and the player.

        :param map_controller: The controller of the maps.
        :param map: The map.
        :param players_position: The tile coordinates of the player's position.
        """

        super().__init__()

        self._map = map
        self._scroller = cocos.layer.ScrollingManager()

        for name, value in map.contents.items():
            if isinstance(value, cocos.tiles.RectMapLayer):
                self._scroller.add(value, z=1)
                if name == MapScene.PLAYER_LAYER_NAME:
                    break

        players_position_pixels = (
            int(MapScene.TILE_SIZE / 2 + players_position[0] * MapScene.TILE_SIZE),
            int(PlayerLayer.CHAR_HEIGHT / 2 + players_position[1] * MapScene.TILE_SIZE)
        )
        self._player_layer = PlayerLayer(map_controller, players_position_pixels)
        self._scroller.add(self._player_layer, z=2)
        self._scroller.set_focus(players_position_pixels[0], players_position_pixels[1])

        has_passed_player_layer = False
        for name, value in map.contents.items():
            if has_passed_player_layer and isinstance(value, cocos.tiles.RectMapLayer):
                self._scroller.add(value, z=3)

            if name == MapScene.PLAYER_LAYER_NAME:
                has_passed_player_layer = True

        self.add(self._scroller)

        self._dialog = Dialog()
        self._dialog.visible = False
        self.add(self._dialog)

        cocos.director.director.replace(self)

    def move_player(self, direction: PlayerDirectionEnum) -> None:
        """Move the player in the given direction.

        :param: direction: The direction of the movement.
        """

        self._player_layer.direction = direction

    def player_handles_event(self, handle: bool = True) -> None:
        """Set whether the player's layer should handle the events.

        :param handle: True if the player's layer should handle the events.
        """

        self._player_layer.is_event_handler = handle

    def pkmn_center_door(self, x: int, y: int) -> None:
        """Animate the pkmn center door opening or closing.

        :param x: The x coordinates of the pkmn center door.
        :param y: The y coordinates of the pkmn center door.
        """

        reverse = True if "pkmn_center_door" in self._scroller.children_names else False

        tileset = pyglet.image.load(PATH + "/assets/map/pkmn_center_door.png")
        tileset_grid = pyglet.image.ImageGrid(tileset, 1, 4, MapScene.TILE_SIZE, tileset.height)
        tileset_anim = pyglet.image.Animation.from_image_sequence(
            reversed(tileset_grid) if reverse else tileset_grid,
            0.1,
            loop=False
        )
        animation = cocos.sprite.Sprite(tileset_anim)
        animation.position = (x + MapScene.TILE_SIZE / 2, y + MapScene.TILE_SIZE + tileset.height / 2)

        scrollable_layer = cocos.layer.ScrollableLayer()
        scrollable_layer.add(animation)

        if reverse:
            self._scroller.remove("pkmn_center_door")
            callback = lambda: self._scroller.remove("pkmn_center_door")
            self.do(Delay(0.4) + CallFunc(callback))

        self._scroller.add(scrollable_layer, z=1, name="pkmn_center_door")

    def tall_grass(self, x: int, y: int) -> None:
        """Animate a tall grass.

        :param x: The x coordinates of the player.
        :param y: The y coordinates of the player.
        """

        tileset = pyglet.image.load(PATH + "/assets/map/tall_grass.png")
        tileset_grid = pyglet.image.ImageGrid(tileset, 1, 3, MapScene.TILE_SIZE, tileset.height)
        tileset_anim = pyglet.image.Animation.from_image_sequence(
            tileset_grid,
            0.1,
            loop=False
        )
        animation = cocos.sprite.Sprite(tileset_anim)
        animation.position = (x + MapScene.TILE_SIZE / 2, y + tileset.height / 2)

        scrollable_layer = cocos.layer.ScrollableLayer()
        scrollable_layer.add(animation)
        self._scroller.add(scrollable_layer, z=2)
        callback = lambda: self._scroller.remove(scrollable_layer)
        self.do(Delay(0.4) + CallFunc(callback))

    def message(self, text_key: str) -> None:
        """Show a message to the player.

        :param text_key: The key of the message.
        """

        self._dialog.visible = True
        self.player_handles_event(False)
        callback = lambda: (setattr(self._dialog, "visible", False), self.player_handles_event(True))
        self._dialog.set_text([I18n().get(text_key)], callback)
