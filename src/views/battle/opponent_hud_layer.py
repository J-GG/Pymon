import cocos
from cocos.actions import *

from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel
from views.common.layer import Layer
from views.common.text import Text
from .hp_bar_color_enum import HPBarColorEnum


class OpponentHUDLayer(Layer):
    """The information about the opponent pokemon: name, level, HP

    Attributes:
        - HP_BAR_SIZE: The size in pixels of the HP bar.
        - HP_UPDATE_DURATION: The time it takes for the HP bar to update.
    """

    HP_BAR_SIZE = 48
    HP_UPDATE_DURATION = 1.3

    def __init__(self, pokemon: PokemonModel) -> None:
        """Create a new HUD showing the opponent pokemon's information.

        :param pokemon: The opponent pokemon.
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
        self._hp_bar.position = -5, -12
        self.add(self._hp_bar)

        for color in HPBarColorEnum:
            if 100 * pokemon.hp // pokemon.stats[StatEnum.HP] <= color.upper_limit:
                self._bar_color = color
                break

        self._hp_bar_size = OpponentHUDLayer.HP_BAR_SIZE * pokemon.hp // pokemon.stats[StatEnum.HP]

        self._hp_bar_content = {color: [] for color in HPBarColorEnum}
        for i in range(OpponentHUDLayer.HP_BAR_SIZE):
            for color in HPBarColorEnum:
                hp_pixel = cocos.sprite.Sprite('img/battle/hud/hp_bar_{0}.png'.format(color.name))
                hp_pixel.position = -22 + i, -12
                hp_pixel.visible = True if color == self._bar_color and i <= self._hp_bar_size else False
                self._hp_bar_content[color].append(hp_pixel)

                self.add(self._hp_bar_content[color][i], z=1)

    def update_hp(self) -> None:
        """Update the size and the color of the HP bar."""

        new_hp_bar_size = OpponentHUDLayer.HP_BAR_SIZE * self._pokemon.hp // self._pokemon.stats[StatEnum.HP]
        time_between_update = OpponentHUDLayer.HP_UPDATE_DURATION / (self._hp_bar_size - new_hp_bar_size)
        step, visible, offset = (1, True, 0) if new_hp_bar_size > self._hp_bar_size else (-1, False, -1)

        for pixel_index in range(self._hp_bar_size + offset, new_hp_bar_size + offset, step):
            self.do(Delay(self._hp_bar_size * time_between_update - time_between_update * pixel_index)
                    + CallFunc(self._toggle_hp_pixel, pixel_index, visible))

        self._hp_bar_size = new_hp_bar_size

    def _toggle_hp_pixel(self, pixel_index: int, visible: bool) -> None:
        """Hide or show the pixel whose the index is specified and changes the color
        of the HP bar if necessary.

        :param pixel_index: The index of the pixel to hide.
        :param visible: Whether the pixel is visible or not
        """

        self._hp_bar_content[self._bar_color][pixel_index].visible = visible
        for color in HPBarColorEnum:
            if pixel_index * 100 // OpponentHUDLayer.HP_BAR_SIZE <= color.upper_limit:
                if color != self._bar_color:
                    self._bar_color = color
                    offset = -1 if visible else 0
                    for i in range(pixel_index + offset):
                        for c in HPBarColorEnum:
                            self._hp_bar_content[c][i].visible = True if c == self._bar_color else False
                break
