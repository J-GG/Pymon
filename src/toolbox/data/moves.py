import json

from models.move import Move
from models.move_category_enum import MoveCategoryEnum
from models.move_effects import MoveEffects
from models.staged_stat_enum import StagedStatEnum
from models.type_enum import TypeEnum
from toolbox.init import PATH

"""This module is meant to load the data regarding the moves available in the 
game.

A JSON file is read and instantiates a ``Move`` for each node of the file.
All the moves are then stored in a dictionary whose the key is the id of the 
move. 
"""

MOVE_ID = "id"
MOVE_TYPE = "type"
MOVE_CATEGORY = "category"
MOVE_POWER = "power"
MOVE_ACCURACY = "accuracy"
MOVE_DEFAULT_PP = "defaultPp"
MOVE_EFFECTS = "effects"
MOVE_STATS = "stats"
MOVE_STATUS = "status"

moves = dict()
with open(PATH + "/assets/data/moves.json") as file:
    json_moves = json.load(file)
    for move in json_moves:
        id = move[MOVE_ID]
        type = TypeEnum[move[MOVE_TYPE]]
        category = MoveCategoryEnum[move[MOVE_CATEGORY]]
        power = move[MOVE_POWER] if MOVE_POWER in move else None
        accuracy = move[MOVE_ACCURACY] if MOVE_ACCURACY in move else None
        default_pp = move[MOVE_DEFAULT_PP]
        effects = None
        if MOVE_EFFECTS in move:
            effects_node = move[MOVE_EFFECTS]
            effects_stats = {StagedStatEnum[name]: value for name, value in effects_node[MOVE_STATS].items()}
            effects_status = effects_node[MOVE_STATUS] if MOVE_STATUS in effects_node else None

            effects = MoveEffects(effects_stats, effects_status)

        moves[id] = Move(id, type, category, power, accuracy, default_pp, effects)
