import typing

import cocos
import pyglet

from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel
from toolbox.i18n import I18n
from toolbox.init import PATH
from views.common.layer import Layer


class StatLayer(Layer):
    """The panel listing the stats.

    If it is displayed after leveling up, the ``gained_levels`` contains by
    how much the stats have increased.
    Whereas if ``gained_levels`` is None, it also displays the current HP.
    """

    stats_color = dict()
    stats_color[StatEnum.HP] = (93, 202, 50, 255)
    stats_color[StatEnum.ATTACK] = (228, 231, 16, 255)
    stats_color[StatEnum.DEFENSE] = (232, 173, 43, 255)
    stats_color[StatEnum.SPECIAL_ATTACK] = (16, 173, 231, 255)
    stats_color[StatEnum.SPECIAL_DEFENSE] = (16, 117, 231, 255)
    stats_color[StatEnum.SPEED] = (198, 16, 231, 255)

    def __init__(self, pokemon: PokemonModel,
                 gained_levels: typing.Union[None, typing.Dict[int, typing.Dict[StatEnum, int]]]) -> None:
        """Create a stat layer.

        :param pokemon: The pokemon whose stats are displayed.
        :param gained_levels: The list of the levels along with, for each stat,
        the amount of the increase.
        """

        super().__init__()

        self._background = cocos.sprite.Sprite(pyglet.image.load(PATH + '/assets/img/common/stats.png'), anchor=(0, 0))
        self.add(self._background)

        stats = {stat: pokemon.stats[stat] for stat in StatEnum}

        if gained_levels:
            for level in gained_levels:
                for stat in StatEnum:
                    stats[stat] -= gained_levels[level][stat]

        i = 0
        for stat in StatEnum:
            stat_label = cocos.text.Label((I18n().get("STAT.{0}".format(stat.name))), bold=True, anchor_x="left",
                                          color=StatLayer.stats_color[stat])
            stat_label.position = (15, 150 - i * 27)
            self.add(stat_label)

            stat_value_str = str(stats[stat]) if gained_levels or stat != StatEnum.HP else "{0} / {1}".format(
                str(pokemon.hp), str(stats[stat]))
            stat_value = cocos.text.Label(stat_value_str, bold=True, anchor_x="center")
            x = 100 if gained_levels else 120
            stat_value.position = (x, 150 - i * 27)
            self.add(stat_value)

            if gained_levels:
                gained_stat = cocos.text.Label("+ {0}".format(next(iter(gained_levels.values()))[stat]), bold=True,
                                               color=(16, 173, 231, 255))
                gained_stat.position = (120, 150 - i * 27)
                self.add(gained_stat)

            i += 1
