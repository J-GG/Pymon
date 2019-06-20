import cocos

from views.map.map_scene import MapScene
from views.map.player_direction_enum import PlayerDirectionEnum


class PkmnCenterDoorEvent:
    """Animate a PKMN Center door on the map."""

    def __init__(self, map_scene: MapScene, x: int, y: int, direction: PlayerDirectionEnum,
                 object: cocos.tiles.TmxObject) -> None:
        """Create an event animating PKMN Center door on the map.

        :param map_scene: The scene containing the map.
        :param x: The x coordinate of the player on the map.
        :param y: The y coordinate of the player on the map.
        :param direction: The direction the player is facing.
        :param object: The object containing all the info about the event.
        """

        if object.px <= x and object.px + object.width > x and object.py <= y and object.py + object.height > y:
            map_scene.pkmn_center_door(object.px, object.py)
