import json

import cocos

from views.map.map_scene import MapScene
from views.map.player_direction_enum import PlayerDirectionEnum


class TeleportEvent:
    """Teleport the player to another map."""

    def __init__(self, map_scene: MapScene, x: int, y: int, direction: PlayerDirectionEnum,
                 object: cocos.tiles.TmxObject) -> None:
        """Create an event to teleport the player to another map.

        :param map_scene: The scene containing the map.
        :param x: The x coordinate of the player on the map.
        :param y: The y coordinate of the player on the map.
        :param direction: The direction the player is facing.
        :param object: The object containing all the info about the event.
        """

        data = dict()
        if object.px <= x and object.px + object.width > x and object.py <= y and object.py + object.height > y:
            data = json.loads(object.properties["teleport"])

        if data:
            map = data["map"]
            i = data["x"]
            j = data["y"]
            required_direction = data["direction"]
            if PlayerDirectionEnum[required_direction] == direction:
                map_scene.teleport(map, (i, j), direction)
