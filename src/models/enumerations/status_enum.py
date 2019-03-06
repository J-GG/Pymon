from enum import Enum


class StatusEnum(Enum):
    """The list of non-volatile status:
    - BURN: The burn condition inflicts damage every turn and halves damage
        dealt by a pokémon's physical moves.
    - FREEZE: The freeze condition causes a Pokémon to be unable to use moves.
    - PARALYSIS: The paralysis condition reduces the pokémon's speed stat and
        causes it to have a 25% chance of being unable to use a move.
    - POISON: The poison condition inflicts damage every turn.
    - SLEEP: The sleep condition  causes a Pokémon to be unable to use moves
        for a randomly chosen duration of 1 to 3 turns.
    """

    BURN = "Burn"
    FREEZE = "Freeze"
    PARALYSIS = "Paralysis"
    POISON = "Poison"
    SLEEP = "Sleep"
