import json
import random

import cocos

from controllers.battle_controller import BattleController
from models.battle.battle_model import BattleModel
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.data.moves import moves
from toolbox.data.pokemon import pokemons
from views.map.map_scene import MapScene
from views.map.player_direction_enum import PlayerDirectionEnum


class WildPokemonEvent:
    """Fight against a wild pokemon."""

    WILD_POKEMON_PROBABILITY = 0.8

    def __init__(self, map_scene: MapScene, x: int, y: int, direction: PlayerDirectionEnum,
                 object: cocos.tiles.TmxObject) -> None:
        """Create an event to fight against a wild pokemon.

        :param map_scene: The scene containing the map.
        :param x: The x coordinate of the player on the map.
        :param y: The y coordinate of the player on the map.
        :param direction: The direction the player is facing.
        :param object: The object containing all the info about the event.
        """

        data = dict()
        if object.px <= x and object.px + object.width > x and object.py <= y and object.py + object.height > y:
            data = json.loads(object.properties["wild_pokemon"])

        if data:
            if random.random() >= WildPokemonEvent.WILD_POKEMON_PROBABILITY:
                wild_pokemons = data["pokemons"]
                place = data["place"]
                prob_pokemon = []
                for pokemon, infos in wild_pokemons.items():
                    prob_pokemon += [pokemon] * infos["probability"]

                random_pokemon = random.choice(prob_pokemon)
                pokemon_species = pokemons[random_pokemon.upper()]
                random_level = random.choice(
                    range(wild_pokemons[random_pokemon]["level_min"], wild_pokemons[random_pokemon]["level_max"] + 1))
                learned_moves = []
                for level, moves_by_lvl_up in pokemon_species.moves_by_lvl_up.items():
                    if level > random_level:
                        break

                    for move in moves_by_lvl_up:
                        learned_moves.append(LearnedMoveModel(moves[move.id], moves[move.id].default_pp,
                                                              moves[move.id].default_pp))
                        if len(learned_moves) >= 4:
                            random.shuffle(learned_moves)
                            learned_moves.pop()

                opponent_pokemons = [PokemonModel(pokemon_species, pokemon_species.name, random_level, learned_moves)]
                BattleController().battle(BattleModel(opponent_pokemons, place),
                                          battle_over_callback=map_scene.player_handles_event)
                map_scene.player_handles_event(False)
