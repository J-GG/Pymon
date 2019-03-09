import typing

import cocos

from models.enumerations.stat_enum import StatEnum
from models.pokemon_model import PokemonModel
from views.common.layer import Layer


class StatLayer(Layer):
    """The panel listing the stats increase after leveling up."""

    def __init__(self, pokemon: PokemonModel, gained_levels: typing.Dict[int, typing.Dict[StatEnum, int]]) -> None:
        """Create a stat layer."""
        super().__init__()

        self._background = cocos.sprite.Sprite('img/battle/stats.png', anchor=(0, 0))
        self.add(self._background)

        stats = {stat: pokemon.stats[stat] for stat in StatEnum}

        for level in gained_levels:
            for stat in StatEnum:
                stats[stat] -= gained_levels[level][stat]

        i = 0
        for stat in StatEnum:
            stat_label = cocos.text.Label(str(stats[stat]), bold=True, anchor_x="center")
            stat_label.position = (100, 150 - i * 27)
            self.add(stat_label)

            gained_stat = cocos.text.Label("+ {0}".format(next(iter(gained_levels.values()))[stat]), bold=True,
                                           color=(16, 173, 231, 255))
            gained_stat.position = (120, 150 - i * 27)
            self.add(gained_stat)

            i += 1
