import cocos

from views.map.map_scene import MapScene
from views.map.player_direction_enum import PlayerDirectionEnum


class MessageEvent:
    """Show a message to the player."""

    def __init__(self, map_scene: MapScene, x: int, y: int, direction: PlayerDirectionEnum,
                 object: cocos.tiles.TmxObject) -> None:
        """Create an event showing a message to the player.

        :param map_scene: The scene containing the map.
        :param x: The x coordinate of the player on the map.
        :param y: The y coordinate of the player on the map.
        :param direction: The direction the player is facing.
        :param object: The object containing all the info about the event.
        """

        if direction == PlayerDirectionEnum.UP:
            players_direction = cocos.tiles.RectMap.UP
        elif direction == PlayerDirectionEnum.DOWN:
            players_direction = cocos.tiles.RectMap.DOWN
        elif direction == PlayerDirectionEnum.RIGHT:
            players_direction = cocos.tiles.RectMap.RIGHT
        else:
            players_direction = cocos.tiles.RectMap.LEFT

        facing_x, facing_y = x + players_direction[0] * MapScene.TILE_SIZE, y + players_direction[
            1] * MapScene.TILE_SIZE

        if object.px <= facing_x and object.px + object.width >= facing_x + MapScene.TILE_SIZE and object.py <= facing_y and object.py + object.height >= facing_y + MapScene.TILE_SIZE:
            map_scene.message(object.properties["message"])
