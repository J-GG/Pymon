import typing

import cocos
import pyglet
from pyglet.window import key

from toolbox.init import PATH
from views.map.player_direction_enum import PlayerDirectionEnum
from .player_action_enum import PlayerActionEnum


class PlayerLayer(cocos.layer.ScrollableLayer):
    """The player on the map."""

    CHARSET_ROWS = 4
    CHARSET_COLUMNS = 4
    ANIMATION_DURATION = 0.4
    CHAR_WIDTH = 64
    CHAR_HEIGHT = 64

    charset = pyglet.image.load(PATH + '/assets/map/player.png')
    charset_grid = pyglet.image.ImageGrid(charset, CHARSET_ROWS, CHARSET_COLUMNS, CHAR_WIDTH, CHAR_HEIGHT)
    charset_fix = dict()
    for direction in PlayerDirectionEnum:
        charset_fix[direction] = pyglet.image.Animation.from_image_sequence(
            charset_grid[direction.value * CHARSET_ROWS:direction.value * CHARSET_ROWS + 1], 1, loop=False
        )
    charset_anim = dict()
    for direction in PlayerDirectionEnum:
        charset_anim[direction] = pyglet.image.Animation.from_image_sequence(
            charset_grid[
            direction.value * CHARSET_ROWS:direction.value * CHARSET_ROWS + CHARSET_COLUMNS] + charset_grid[
                                                                                               direction.value * CHARSET_ROWS:direction.value * CHARSET_ROWS + 1],
            ANIMATION_DURATION / (CHARSET_COLUMNS + 1),
            loop=False
        )

    cocos.director.director.window.pop_handlers()
    keyboard = key.KeyStateHandler()
    cocos.director.director.window.push_handlers(keyboard)

    def __init__(self, map_controller, players_position_pixels: typing.Tuple[int, int]) -> None:
        """Create the player layer.

        :param map_controller: The map controller.
        :param players_position: The coordinates of the player on the map in pixels.
        """

        super().__init__()

        self._map_controller = map_controller
        self._direction = PlayerDirectionEnum.DOWN
        self._time_left_moving = 0

        self._sprite = cocos.sprite.Sprite(PlayerLayer.charset_fix[self.direction])
        self._sprite.position = (players_position_pixels[0], players_position_pixels[1])
        self._sprite.velocity = (0, 0)
        self._sprite.do(PlayerMovement())
        self.add(self._sprite)

        self._final_position = (players_position_pixels[0], players_position_pixels[1])

    def _move(self, change_direction: bool = False) -> None:
        """Update the player's sprite according to his direction.

        :param change_direction: True if the direction has changed.
        """

        position = self._sprite.position
        self.remove(self._sprite)

        if change_direction:
            self._sprite = cocos.sprite.Sprite(PlayerLayer.charset_fix[self.direction])
            self._sprite.position = position
            self._sprite.velocity = (0, 0)
            self._sprite.do(PlayerMovement())
            self.add(self._sprite)
            self.time_left_moving = 0
        else:
            self._sprite = cocos.sprite.Sprite(PlayerLayer.charset_anim[self.direction])
            self._sprite.position = position
            self._sprite.velocity = (0, 0)
            self._sprite.do(PlayerMovement())
            self.add(self._sprite)
            self.time_left_moving = (PlayerLayer.ANIMATION_DURATION / (
                    PlayerLayer.CHARSET_COLUMNS + 1) * PlayerLayer.CHARSET_COLUMNS)

            right_left = 1 if self.direction == PlayerDirectionEnum.RIGHT else -1 if self.direction == PlayerDirectionEnum.LEFT else 0
            up_down = 1 if self.direction == PlayerDirectionEnum.UP else -1 if self.direction == PlayerDirectionEnum.DOWN else 0

            vel_x = right_left * self.parent.parent.TILE_SIZE * 1 / (PlayerLayer.ANIMATION_DURATION / (
                    PlayerLayer.CHARSET_COLUMNS + 1) * PlayerLayer.CHARSET_COLUMNS)
            vel_y = up_down * self.parent.parent.TILE_SIZE * 1 / (PlayerLayer.ANIMATION_DURATION / (
                    PlayerLayer.CHARSET_COLUMNS + 1) * PlayerLayer.CHARSET_COLUMNS)
            self._sprite.velocity = (vel_x, vel_y)
            self._final_position = (
                self._final_position[0] + right_left * self.parent.parent.TILE_SIZE,
                self._final_position[1] + up_down * self.parent.parent.TILE_SIZE
            )

    @property
    def map_controller(self):
        """Get the controller of the map.

        :return: The ``MapController``.
        """

        return self._map_controller

    @property
    def direction(self) -> PlayerDirectionEnum:
        """Get the direction the player is facing.

        :return: The ``PlayerDirectionEnum``.
        """

        return self._direction

    @direction.setter
    def direction(self, direction) -> None:
        """Set the direction the player is facing.

        :param direction: The ``PlayerDirectionEnum``.
        """

        if self._direction != direction:
            self._direction = direction
            self._move(True)
        else:
            self._move()

    @property
    def final_position(self) -> typing.Tuple[int, int]:
        """Get the coordinates of the player's final position, after the movement.

        :return: The coordinates of the final position.
        """

        return self._final_position

    @property
    def time_left_moving(self) -> int:
        """Get the time left for the player to finish his movement.

        :return: The time left in seconds.
        """

        return self._time_left_moving

    @time_left_moving.setter
    def time_left_moving(self, time_left_moving) -> None:
        """Set the time left for the player to finish his movement.

        :param time_left_moving: The time left in seconds.
        """

        self._time_left_moving = time_left_moving


class PlayerMovement(cocos.actions.Move):
    """Manages the player's actions."""

    def step(self, dt: int) -> None:
        super().step(dt)

        if self.target.parent.time_left_moving == 0:
            if PlayerLayer.keyboard[key.RIGHT] or PlayerLayer.keyboard[key.LEFT] or PlayerLayer.keyboard[key.UP] or \
                    PlayerLayer.keyboard[key.DOWN]:
                if PlayerLayer.keyboard[key.UP]:
                    direction = PlayerDirectionEnum.UP
                elif PlayerLayer.keyboard[key.LEFT]:
                    direction = PlayerDirectionEnum.LEFT
                elif PlayerLayer.keyboard[key.RIGHT]:
                    direction = PlayerDirectionEnum.RIGHT
                else:
                    direction = PlayerDirectionEnum.DOWN

                self.target.parent.map_controller.action(
                    self.target.position,
                    self.target.parent.direction,
                    PlayerActionEnum.PLAYER_START_MOVE,
                    **{"new_direction": direction}
                )
            elif PlayerLayer.keyboard[key.ENTER]:
                self.target.parent.map_controller.action(
                    self.target.position,
                    self.target.parent.direction,
                    PlayerActionEnum.ACTION_BUTTON,
                )
        else:
            self.target.parent.time_left_moving -= dt
            if self.target.parent.time_left_moving <= 0:
                self.target.parent.time_left_moving = 0
                self.target.velocity = (0, 0)
                self.target.position = self.target.parent.final_position
                self.target.parent.map_controller.action(
                    self.target.position,
                    self.target.parent.direction,
                    PlayerActionEnum.PLAYER_END_MOVE
                )

        self.target.parent.parent.set_focus(self.target.x, self.target.y)