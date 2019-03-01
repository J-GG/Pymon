from enum import Enum


class ActionEnum(Enum):
    """The list of actions available to the player in a battle."""
    
    FIGHT = 3
    BAG = 2
    PKMN = 1
    RUN = 0
