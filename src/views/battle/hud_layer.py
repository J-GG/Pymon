import typing
from math import ceil

import cocos
import pyglet
from cocos.actions import *

from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel
from toolbox.init import PATH
from views.common.layer import Layer
from views.common.text import Text
from .hp_bar_color_enum import HPBarColorEnum


class HUDLayer(Layer):
    """The information about the player's pokemon: name, level, HP, XP

    Attributes:
        - HP_BAR_SIZE: The size in pixels of the HP bar.
        - HP_UPDATE_DURATION: The time it takes for the HP bar to update.
        - XP_BAR_SIZE: The size in pixels of the XP bar.
        - XP_UPDATE_DURATION: The time it takes for the XP bar to update.
    """

    HP_BAR_SIZE = 48
    HP_UPDATE_DURATION = 1.3
    XP_BAR_SIZE = 93
    XP_UPDATE_DURATION = 1

    def __init__(self, pokemon: PokemonModel, forced_hp: int = None) -> None:
        """Create a new HUD showing the player's pokemon's information.
        The ``hp`` parameter is only useful if the current number of HP is
        different from the displayed one.

        :param pokemon: The player's pokemon.
        :param forced_hp: The number of HP to display.
        """

        super().__init__()
        self._pokemon = pokemon

        hp = forced_hp if forced_hp else pokemon.hp
        self._name = Text(pokemon.nickname)
        self._name.position = -self._name.width, 0
        self.add(self._name, z=1)

        self._level_txt = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/battle/hud/level.png'))
        self._level_txt.position = 5, -2
        self.add(self._level_txt, z=1)

        self._level = Text(str(pokemon.level))
        self._level.position = 17, 0
        self.add(self._level, z=1)

        self._hp_bar = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/battle/hud/hp_bar.png'))
        self._hp_bar.position = -6, -12
        self.add(self._hp_bar)

        for color in HPBarColorEnum:
            if ceil(100 * pokemon.hp / pokemon.stats[StatEnum.HP]) <= color.upper_limit:
                self._bar_color = color
                break

        self._hp_bar_size = ceil(HUDLayer.HP_BAR_SIZE * hp / pokemon.stats[StatEnum.HP])

        self._hp_bar_content = {color: [] for color in HPBarColorEnum}
        for i in range(HUDLayer.HP_BAR_SIZE):
            for color in HPBarColorEnum:
                hp_pixel = cocos.sprite.Sprite(
                    pyglet.image.load(PATH + '/assets/img/battle/hud/hp_bar_{0}.png'.format(color.name)))
                hp_pixel.position = -23 + i, -12
                hp_pixel.visible = True if color == self._bar_color and i < self._hp_bar_size else False
                self._hp_bar_content[color].append(hp_pixel)

                self.add(self._hp_bar_content[color][i], z=1)

        self._hp = Text("{0}/{1}".format(hp, pokemon.stats[StatEnum.HP]))
        self._hp.position = -20, -24
        self.add(self._hp, z=1)

        self._xp_bar = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/battle/hud/xp_bar.png'))
        self._xp_bar.position = -10, -37
        self.add(self._xp_bar)

        xp_current_lvl = self._pokemon.species.experience_function.get_xp_for_level(self._pokemon.level)
        self._xp_bar_content = []
        self._xp_bar_size = HUDLayer.XP_BAR_SIZE * (pokemon.experience - xp_current_lvl) // (
                pokemon.experience_for_next_level - xp_current_lvl)
        for i in range(HUDLayer.XP_BAR_SIZE):
            self._xp_bar_content.append(
                cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/battle/hud/xp_bar_blue.png')))
            self._xp_bar_content[i].position = -56 + i, -37
            self._xp_bar_content[i].visible = False if i > self._xp_bar_size else True
            self.add(self._xp_bar_content[i], z=1)

    def update_hp(self) -> None:
        """Update the size and the color of the HP bar as well as the HP
        number.
        """

        new_hp_bar_size = ceil(HUDLayer.HP_BAR_SIZE * self._pokemon.hp / self._pokemon.stats[StatEnum.HP])
        hp_per_pixel = self._pokemon.stats[StatEnum.HP] / HUDLayer.HP_BAR_SIZE
        if new_hp_bar_size != self._hp_bar_size:
            time_between_update = HUDLayer.HP_UPDATE_DURATION / abs(self._hp_bar_size - new_hp_bar_size)
            start = 0 if self._hp_bar_size <= 0 else self._hp_bar_size - 1
            step, visible, stop = (1, True, new_hp_bar_size) if new_hp_bar_size > self._hp_bar_size else (
                -1, False, new_hp_bar_size - 1)
            i = 0

            for pixel_index in range(start, stop, step):
                self.do(Delay(i * time_between_update)
                        + (CallFunc(self._toggle_hp_pixel, pixel_index, visible)
                           | CallFunc(self._update_hp_number, ceil(hp_per_pixel * pixel_index),
                                      self._pokemon.stats[StatEnum.HP]))
                        )
                i += 1
            self._hp_bar_size = new_hp_bar_size

        self.do(Delay(HUDLayer.HP_UPDATE_DURATION + 0.1) + CallFunc(self._update_hp_number, self._pokemon.hp,
                                                                    self._pokemon.stats[StatEnum.HP]))

    def _update_hp_number(self, hp: int, max_hp: int) -> None:
        """Update the textual number of HP.

        :param hp: The number of HP to display.
        :param max_hp: The number of maximal HP to display.
        """

        hp = 0 if hp < 0 else hp

        self.remove(self._hp)
        self._hp = Text("{0}/{1}".format(hp, max_hp))
        self._hp.position = -20, -24
        self.add(self._hp, z=1)

    def _toggle_hp_pixel(self, pixel_index: int, visible: bool) -> None:
        """Hide or show the pixel whose the index is specified and changes the color
        of the HP bar if necessary.

        :param pixel_index: The index of the pixel to hide.
        :param visible: Whether the pixel is visible or not
        """

        self._hp_bar_content[self._bar_color][pixel_index].visible = visible
        for color in HPBarColorEnum:
            if ceil(pixel_index * 100 / HUDLayer.HP_BAR_SIZE) <= color.upper_limit:
                if color != self._bar_color:
                    self._bar_color = color
                    stop = pixel_index + 1 if visible else pixel_index
                    for i in range(stop):
                        for c in HPBarColorEnum:
                            self._hp_bar_content[c][i].visible = True if c == self._bar_color else False
                break

    def update_xp(self, level_up_stats: typing.Union[typing.Dict, None] = None) -> None:
        """Update the size of the XP bar and update the number of HP after
        leveling up.

        :param level_up_stats: The stats increase associated with the optional
        level up.
        """

        xp_current_lvl = self._pokemon.species.experience_function.get_xp_for_level(self._pokemon.level)

        if level_up_stats:
            new_xp_bar_size = HUDLayer.XP_BAR_SIZE
        else:
            new_xp_bar_size = ceil(HUDLayer.XP_BAR_SIZE * (self._pokemon.experience - xp_current_lvl) / (
                    self._pokemon.experience_for_next_level - xp_current_lvl))

        if new_xp_bar_size != self._xp_bar_size:
            time_between_update = HUDLayer.XP_UPDATE_DURATION / (new_xp_bar_size - self._xp_bar_size)

            for pixel_index in range(self._xp_bar_size, new_xp_bar_size, 1):
                self._xp_bar_content[pixel_index].do(
                    Delay(time_between_update * (pixel_index - self._xp_bar_size))
                    + CallFunc(self._toggle_xp_pixel, pixel_index, True))

            if level_up_stats:
                self._level.do(Delay(HUDLayer.XP_UPDATE_DURATION) + CallFunc(self._update_level))
                hp = int(self._hp.text.split("/")[0]) + level_up_stats[StatEnum.HP]
                max_hp = int(self._hp.text.split("/")[1]) + level_up_stats[StatEnum.HP]
                self._hp.do(Delay(HUDLayer.XP_UPDATE_DURATION)
                            + CallFunc(self._update_hp_number, hp, max_hp))
                new_hp_bar_size = HUDLayer.HP_BAR_SIZE * hp // max_hp
                for pixel_index in range(new_hp_bar_size):
                    self._hp.do(Delay(HUDLayer.XP_UPDATE_DURATION) + CallFunc(self._toggle_hp_pixel, pixel_index, True))

            self._xp_bar_size = new_xp_bar_size

    def _update_level(self) -> None:
        """Update the level."""

        self.remove(self._level)
        self._level = Text(str(int(self._level.text) + 1))
        self._level.position = 17, 0
        self.add(self._level, z=1)

    def reset_xp_bar(self) -> None:
        """Hide all of the pixels of the XP bar."""

        for pixel_index in range(HUDLayer.XP_BAR_SIZE):
            self._toggle_xp_pixel(pixel_index, False)

        self._xp_bar_size = 0

    def _toggle_xp_pixel(self, pixel_index: int, visible: bool) -> None:
        """Hide or show the pixel of the xp bar whose the index is specified.

        :param pixel_index: The index of the pixel to hide.
        :param visible: Whether the pixel is visible or not
        """

        self._xp_bar_content[pixel_index].visible = visible
