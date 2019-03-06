import cocos
from cocos.actions import *

from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel
from views.common.layer import Layer
from views.common.text import Text
from .hp_bar_color_enum import HPBarColorEnum


class HUDLayer(Layer):
    """The information about the player's pokemon: name, level, HP, XP

        Attributes:
        - HP_BAR_SIZE: The size in pixels of the HP bar.
    """

    HP_BAR_SIZE = 48

    def __init__(self, pokemon: PokemonModel) -> None:
        """Create a new HUD showing the player's pokemon's information.

        :param pokemon: The player's pokemon.
        """

        super().__init__()
        self._pokemon = pokemon

        self._name = Text(pokemon.nickname)
        self._name.position = -self._name.width, 0
        self.add(self._name, z=1)

        self._level_txt = cocos.sprite.Sprite('img/battle/hud/level.png')
        self._level_txt.position = 5, -2
        self.add(self._level_txt, z=1)

        self._level = Text(str(pokemon.level))
        self._level.position = 17, 0
        self.add(self._level, z=1)

        self._hp_bar = cocos.sprite.Sprite('img/battle/hud/hp_bar.png')
        self._hp_bar.position = -6, -12
        self.add(self._hp_bar)

        for color in HPBarColorEnum:
            if 100 * pokemon.hp // pokemon.stats[StatEnum.HP] <= color.upper_limit:
                self._bar_color = color
                break

        self._hp_bar_size = HUDLayer.HP_BAR_SIZE * pokemon.hp // pokemon.stats[StatEnum.HP]

        self._hp_bar_content = {color: [] for color in HPBarColorEnum}
        for i in range(HUDLayer.HP_BAR_SIZE):
            for color in HPBarColorEnum:
                hp_pixel = cocos.sprite.Sprite('img/battle/hud/hp_bar_{0}.png'.format(color.name))
                hp_pixel.position = -23 + i, -12
                hp_pixel.visible = True if color == self._bar_color and i <= self._hp_bar_size else False
                self._hp_bar_content[color].append(hp_pixel)

                self.add(self._hp_bar_content[color][i], z=1)

        self._hp = Text("{0}/{1}".format(pokemon.hp, pokemon.stats[StatEnum.HP]))
        self._hp.position = -20, -24
        self.add(self._hp, z=1)

        self._xp_bar = cocos.sprite.Sprite('img/battle/hud/xp_bar.png')
        self._xp_bar.position = -10, -37
        self.add(self._xp_bar)

        self._current_xp_bar = []
        current_xp_bar_size = 93 * (pokemon.experience - pokemon.species.experience_function.get_xp_for_level(
            pokemon.level)) // (
                                      pokemon.experience_for_next_level - pokemon.species.experience_function.get_xp_for_level(
                                  pokemon.level))
        for i in range(current_xp_bar_size):
            self._current_xp_bar.append(cocos.sprite.Sprite('img/battle/hud/xp_bar_blue.png'))
            self._current_xp_bar[i].position = 390 + i, 195
            self.add(self._current_xp_bar[i], z=1)

    def update_hp(self) -> None:
        """Update the size and the color of the HP bar."""

        new_hp_bar_size = HUDLayer.HP_BAR_SIZE * self._pokemon.hp // self._pokemon.stats[StatEnum.HP]

        for pixel_index in range(self._hp_bar_size - 1, -1, -1):
            if pixel_index > new_hp_bar_size:
                self.do(
                    Delay(self._hp_bar_size * 0.1 - 0.1 * pixel_index) + CallFunc(self.hide_hp_pixel, pixel_index))

        self._hp_bar_size = new_hp_bar_size

    def hide_hp_pixel(self, pixel_index: int) -> None:
        """Hide the pixel whose the index is specified and changes the color
        of the HP bar if necessary.

        :param pixel_index: the index of the current pixel.
        """

        self._hp_bar_content[self._bar_color][pixel_index].visible = False
        for color in HPBarColorEnum:
            if pixel_index * 100 // HUDLayer.HP_BAR_SIZE <= color.upper_limit:
                if color != self._bar_color:
                    self._bar_color = color
                    for i in range(pixel_index):
                        for c in HPBarColorEnum:
                            self._hp_bar_content[c][i].visible = True if c == self._bar_color else False
                break
