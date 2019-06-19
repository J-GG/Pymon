import cocos

from views.map.map_scene import MapScene
from views.map.player_direction_enum import PlayerDirectionEnum


class MoveEvent:
    """Move the player."""

    def __init__(self, map_scene: MapScene, x: int, y: int, direction: PlayerDirectionEnum,
                 new_direction: PlayerDirectionEnum, map: cocos.tiles.Resource) -> None:
        """Create an event to move the player.

        :param map_scene: The scene containing the map.
        :param x: The x coordinate of the player on the map.
        :param y: The y coordinate of the player on the map.
        :param direction: The direction the player is facing.
        :param new_direction: The new direction the player wants to move to.
        :param map: The map.
        """

        if direction == PlayerDirectionEnum.UP:
            players_direction = cocos.tiles.RectMap.UP
        elif direction == PlayerDirectionEnum.DOWN:
            players_direction = cocos.tiles.RectMap.DOWN
        elif direction == PlayerDirectionEnum.RIGHT:
            players_direction = cocos.tiles.RectMap.RIGHT
        else:
            players_direction = cocos.tiles.RectMap.LEFT

        if new_direction != direction:
            move = True
        else:
            walkable = True
            for key, value in map.contents.items():
                if isinstance(value, cocos.tiles.RectMapLayer):
                    cell = value.get_neighbor(value.get_at_pixel(x, y), players_direction)
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
            map_scene.move_player(new_direction)
