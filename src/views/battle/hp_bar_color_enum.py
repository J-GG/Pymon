import cocos
from cocos.actions import *

from views.battle.actions_enum import ActionEnum
from views.common.key_enum import KeyEnum
from views.common.layer import Layer
from enum import Enum


class HPBarColorEnum(Enum):
    RED = "red", 20
    YELLOW = "yellow", 50
    GREEN = "green", 100

    def __init__(self, name, upper_limit):
        super().__init__()
        self._name = name
        self._upper_limit = upper_limit

    @property
    def name(self):
        return self._name

    @property
    def upper_limit(self):
        return self._upper_limit
