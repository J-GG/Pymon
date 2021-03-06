import json

from models.enumerations.experience_function_enum import ExperienceFunctionEnum
from models.enumerations.stat_enum import StatEnum
from models.enumerations.type_enum import TypeEnum
from models.pokemon_species_model import PokemonSpeciesModel
from toolbox.init import PATH
from .moves import moves

"""This module is meant to load the data regarding the pokemon available in the 
game.

A JSON file is read and instantiates a ``Pokemon`` for each node of the file.
All the pokemon are then stored in a dictionary whose the key is the id of the 
pokemon. 
"""

POKEMON_ID = "id"
POKEMON_TYPE = "type"
POKEMON_BASE_STATS = "baseStats"
POKEMON_BASE_EXPERIENCE = "baseExperience"
POKEMON_EXPERIENCE_FUNCTION = "experienceFunction"
POKEMON_MOVES_BY_LVL_UP = "movesByLvlUp"

pokemons = dict()
with open(PATH + "/assets/data/pokemon.json") as file:
    json_pokemon = json.load(file)
    for pokemon in json_pokemon:
        id = pokemon[POKEMON_ID]
        type = [TypeEnum[type] for type in pokemon[POKEMON_TYPE]]
        base_stats = {StatEnum[name]: value for name, value in pokemon[POKEMON_BASE_STATS].items()}
        base_experience = pokemon[POKEMON_BASE_EXPERIENCE]
        experience_function = ExperienceFunctionEnum[pokemon[POKEMON_EXPERIENCE_FUNCTION]]
        moves_by_lvl_up = dict()
        for (lvl, movesList) in pokemon[POKEMON_MOVES_BY_LVL_UP].items():
            moves_by_lvl_up[int(lvl)] = [moves[move] for move in movesList]

        pokemons[id] = PokemonSpeciesModel(id, type, moves_by_lvl_up, base_stats, base_experience, experience_function)
