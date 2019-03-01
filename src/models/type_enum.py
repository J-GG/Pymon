from enum import Enum


class TypeEnum(Enum):
    """The list of types.

    Pokemon can have one or two types and moves have one type.

    The attribute ``no_effect``, ``not_effective``and ``super_effective``
    indicates the effectiveness of a move, influencing greatly how much damage
    moves inflict:
    - If the type of a move is super effective against a type of its target,
        the damage done is double the normal amount.
    - If the type of a move is not very effective against a type of its target,
        the damage done is half the normal amount.
    - If the type of a move is not effective against a type of its target, the
        target is completely immune to it, and the move will deal no damage.

    For targets that have two types, overall type effectiveness is the combined
        effectiveness against each of its types:
    - If the type of a move is super effective against both of the opponent's
        types, then the move does 4 times the damage.
    - If the type of a move is not very effective against both of the
        opponent's types, then the move only does ¼ of the damage.
    - If the type of a move is super effective against one of the opponent's
        types but not very effective against the other, then the move deals
        normal damage.
    - If the type of move is completely ineffective against one of the
        opponent's types, then the move does no damage, even if the opponent has a
        second type that would be vulnerable to it.
    """

    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    ELECTRIC = "Electric"
    GRASS = "Grass"
    ICE = "Ice"
    FIGHT = "Fight"
    FLYING = "Flying"
    POISON = "Poison"
    GROUND = "Ground"
    PSYCHIC = "Psychic"
    ROCK = "Rock"
    BUG = "Bug"
    DRAGON = "Dragon"
    GHOST = "Ghost"
    DARK = "Dark"
    STEEL = "Steel"
    FAIRY = "Fairy"

    def __init__(self, value):
        self._value = value

        self._no_effect = []
        self._not_effective = []
        self._super_effective = []

    @property
    def no_effect(self):
        return self._no_effect

    @no_effect.setter
    def no_effect(self, no_effect):
        self._no_effect = no_effect

    @property
    def not_effective(self):
        return self._not_effective

    @not_effective.setter
    def not_effective(self, not_effective):
        self._not_effective = not_effective

    @property
    def super_effective(self):
        return self._super_effective

    @super_effective.setter
    def super_effective(self, super_effective):
        self._super_effective = super_effective

    def effectiveness(self, defense_types):
        """Determines the effectiveness of a move of this type against
            one or several of the defending type.

        :param defense_types: A list of types of the opponent.
        :return: The multiplier of the move.
        """
        multiplier = 1
        for type in defense_types:
            if type in self._no_effect:
                multiplier = 0
                break
            elif type in self._not_effective:
                multiplier *= 1 / 2
            elif type in self._super_effective:
                multiplier *= 2

        return multiplier


TypeEnum.NORMAL.no_effect = [TypeEnum.GHOST]
TypeEnum.NORMAL.not_effective = [TypeEnum.ROCK, TypeEnum.STEEL]

TypeEnum.FIRE.not_effective = [TypeEnum.FIRE, TypeEnum.WATER, TypeEnum.ROCK,
                               TypeEnum.DRAGON]
TypeEnum.FIRE.super_effective = [TypeEnum.GRASS, TypeEnum.ICE, TypeEnum.BUG,
                                 TypeEnum.STEEL]

TypeEnum.WATER.not_effective = [TypeEnum.WATER, TypeEnum.GRASS, TypeEnum.DRAGON]
TypeEnum.WATER.super_effective = [TypeEnum.FIRE, TypeEnum.GROUND, TypeEnum.ROCK]

TypeEnum.ELECTRIC.no_effect = [TypeEnum.GROUND]
TypeEnum.ELECTRIC.not_effective = [TypeEnum.ELECTRIC, TypeEnum.GRASS, TypeEnum.DRAGON]
TypeEnum.ELECTRIC.super_effective = [TypeEnum.WATER, TypeEnum.FLYING]

TypeEnum.GRASS.not_effective = [TypeEnum.FIRE, TypeEnum.GRASS, TypeEnum.POISON,
                                TypeEnum.FLYING, TypeEnum.BUG, TypeEnum.DRAGON,
                                TypeEnum.STEEL]
TypeEnum.GRASS.super_effective = [TypeEnum.WATER, TypeEnum.GROUND, TypeEnum.ROCK]
TypeEnum.ICE.not_effective = [TypeEnum.FIRE, TypeEnum.STEEL, TypeEnum.WATER,
                              TypeEnum.PSYCHIC]
TypeEnum.ICE.super_effective = [TypeEnum.FLYING, TypeEnum.ROCK, TypeEnum.GRASS,
                                TypeEnum.DRAGON]
TypeEnum.FIGHT.no_effect = [TypeEnum.GHOST]
TypeEnum.FIGHT.not_effective = [TypeEnum.FLYING, TypeEnum.POISON, TypeEnum.BUG,
                                TypeEnum.PSYCHIC, TypeEnum.FAIRY]
TypeEnum.FIGHT.super_effective = [TypeEnum.NORMAL, TypeEnum.ROCK, TypeEnum.STEEL,
                                  TypeEnum.ICE, TypeEnum.DARK]
TypeEnum.FLYING.not_effective = [TypeEnum.ROCK, TypeEnum.STEEL, TypeEnum.ELECTRIC]
TypeEnum.FLYING.super_effective = [TypeEnum.FIGHT, TypeEnum.BUG, TypeEnum.GRASS,
                                   TypeEnum.DRAGON]
TypeEnum.POISON.no_effect = [TypeEnum.STEEL]
TypeEnum.POISON.not_effective = [TypeEnum.POISON, TypeEnum.GROUND, TypeEnum.ROCK,
                                 TypeEnum.GHOST]
TypeEnum.POISON.super_effective = [TypeEnum.GRASS, TypeEnum.FAIRY]
TypeEnum.GROUND.no_effect = [TypeEnum.FLYING]
TypeEnum.GROUND.not_effective = [TypeEnum.GRASS, TypeEnum.BUG]
TypeEnum.GROUND.super_effective = [TypeEnum.POISON, TypeEnum.ROCK, TypeEnum.STEEL,
                                   TypeEnum.FIRE, TypeEnum.ELECTRIC]
TypeEnum.PSYCHIC.no_effect = [TypeEnum.DARK]
TypeEnum.PSYCHIC.not_effective = [TypeEnum.STEEL, TypeEnum.PSYCHIC]
TypeEnum.PSYCHIC.super_effective = [TypeEnum.POISON, TypeEnum.FIGHT]
TypeEnum.ROCK.no_effect = [TypeEnum.DARK]
TypeEnum.ROCK.not_effective = [TypeEnum.FIGHT, TypeEnum.GROUND, TypeEnum.STEEL]
TypeEnum.ROCK.super_effective = [TypeEnum.FLYING, TypeEnum.BUG, TypeEnum.FIRE,
                                 TypeEnum.ICE]
TypeEnum.BUG.not_effective = [TypeEnum.FIGHT, TypeEnum.FLYING, TypeEnum.POISON,
                              TypeEnum.GHOST, TypeEnum.STEEL, TypeEnum.FIRE,
                              TypeEnum.FAIRY]
TypeEnum.BUG.super_effective = [TypeEnum.GRASS, TypeEnum.PSYCHIC, TypeEnum.DARK]
TypeEnum.DRAGON.no_effect = [TypeEnum.FAIRY]
TypeEnum.DRAGON.not_effective = [TypeEnum.STEEL]
TypeEnum.DRAGON.super_effective = [TypeEnum.DRAGON]
TypeEnum.GHOST.no_effect = [TypeEnum.NORMAL]
TypeEnum.GHOST.not_effective = [TypeEnum.DARK]
TypeEnum.GHOST.super_effective = [TypeEnum.GHOST, TypeEnum.PSYCHIC]
TypeEnum.DARK.no_effect = [TypeEnum.NORMAL]
TypeEnum.DARK.not_effective = [TypeEnum.DARK, TypeEnum.FIGHT, TypeEnum.FAIRY]
TypeEnum.DARK.super_effective = [TypeEnum.GHOST, TypeEnum.PSYCHIC]
TypeEnum.STEEL.not_effective = [TypeEnum.STEEL, TypeEnum.FIRE, TypeEnum.WATER,
                                TypeEnum.ELECTRIC]
TypeEnum.STEEL.super_effective = [TypeEnum.ROCK, TypeEnum.ICE, TypeEnum.FAIRY]
TypeEnum.FAIRY.not_effective = [TypeEnum.POISON, TypeEnum.STEEL, TypeEnum.FIRE]
TypeEnum.FAIRY.super_effective = [TypeEnum.FIGHT, TypeEnum.DRAGON, TypeEnum.DARK]
