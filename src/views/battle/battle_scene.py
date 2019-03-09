import importlib
import random
import typing

import cocos
from cocos.actions import *

from models.battle.fight_action_model import FightActionModel
from models.battle.run_action_model import RunActionModel
from models.enumerations.move_category_enum import MoveCategoryEnum
from models.enumerations.move_effectiveness_enum import MoveEffectivenessEnum
from models.enumerations.stat_enum import StatEnum
from models.learned_move_model import LearnedMoveModel
from models.pokemon_model import PokemonModel
from toolbox.i18n import I18n
from views.common.dialog import Dialog
from .actions_layer import ActionsLayer
from .background_layer import BackgroundLayer
from .fade_layer import FadeLayer
from .hud_layer import HUDLayer
from .moves_layer import MovesLayer
from .opponent_hud_layer import OpponentHUDLayer
from .opponent_pokemon_layer import OpponentPokemonLayer
from .pokemon_layer import PokemonLayer
from .stat_layer import StatLayer
from .transition_layer import TransitionLayer


class BattleScene(cocos.scene.Scene):
    """The battle opposing two pokemon.

    Attributes:
        - BATTLE_TRANSITIONS: contains all of the transitions allowed between a
            scene and the battle scene.
        - TRANSITION_DURATION: How long the transition is visible in seconds.
        - TRAVELING_DURATION: How long the traveling on the opponent is.
        - ZOOM_OUT_DURATION: How long the traveling from the opponent to the
            player's pokemon is.
    """

    BATTLE_TRANSITIONS = ["FadeTransition", "SplitColsTransition", "SplitRowsTransition", "FadeDownTransition",
                          "FadeUpTransition", "FadeBLTransition", "FadeTRTransition", "TurnOffTilesTransition"]
    TRANSITION_DURATION = 2
    TRAVELING_DURATION = 2
    ZOOM_OUT_DURATION = 1

    def __init__(self, battle_controller, players_pokemon: PokemonModel, opponent_pokemon: PokemonModel) -> None:
        """Create a battle scene.

        :param battle_controller: The controller to be called to manage.
        :param players_pokemon: The player's pokemon.
        :param opponent_pokemon: The opponent pokemon.
        """

        super().__init__()
        self._battle_controller = battle_controller
        self._players_pokemon = players_pokemon
        self._opponent_pokemon = opponent_pokemon

        transition_class = getattr(importlib.import_module("cocos.scenes.transitions"),
                                   random.choice(BattleScene.BATTLE_TRANSITIONS))
        cocos.director.director.replace(transition_class(self))

        self._intro()

    def _intro(self) -> None:
        """The "cinematic" showing the battle field and the pokemon."""

        self._transition = TransitionLayer()
        self._transition.do(
            Delay(BattleScene.TRANSITION_DURATION * 2 / 3) +
            (ScaleTo(3.5, BattleScene.TRANSITION_DURATION * 1 / 3) | FadeOut(BattleScene.TRANSITION_DURATION * 1 / 3)))
        self.add(self._transition, z=100)

        self._background = BackgroundLayer()
        self._background.scale = 2
        self._background.position = (160, 240)
        self._background.do(Delay(BattleScene.TRANSITION_DURATION * 2 / 3)
                            + MoveBy((250, 0), BattleScene.TRAVELING_DURATION)
                            + MoveTo((160, 240), 0)
                            + (ScaleTo(1, BattleScene.ZOOM_OUT_DURATION)
                               | MoveTo((260, 240), BattleScene.ZOOM_OUT_DURATION))
                            )
        self.add(self._background)

        self._dialog = Dialog()
        self._dialog.do(Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION / 2 + 0.2)
                        + FadeOut(0)
                        + Delay(BattleScene.ZOOM_OUT_DURATION - 0.2)
                        )
        self._dialog.set_text(I18n().get("BATTLE.WILD").format(self._opponent_pokemon.nickname))
        self.add(self._dialog, z=50)

        self._opponent_pokemonLayer = OpponentPokemonLayer(self._opponent_pokemon)
        self._opponent_pokemonLayer.scale = 2
        self._opponent_pokemonLayer.position = (720, 380)
        self._opponent_pokemonLayer.do(Delay(BattleScene.TRANSITION_DURATION * 2 / 3)
                                       + MoveBy((250, 0), BattleScene.TRAVELING_DURATION)
                                       + MoveTo((720, 380), 0)
                                       + (ScaleTo(1, BattleScene.ZOOM_OUT_DURATION) | MoveBy((-180, -70),
                                                                                             BattleScene.ZOOM_OUT_DURATION))
                                       )
        self.add(self._opponent_pokemonLayer)

        self._fade = FadeLayer()
        self._fade.do(Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION / 2)
                      + FadeIn(0.2)
                      + FadeOut(1)
                      )
        self.add(self._fade, z=100)

        self._pokemon = PokemonLayer(self._players_pokemon)
        self._pokemon.scale = 2.5
        self._pokemon.position = (150, 150)
        self._pokemon.do(
            Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION * 2 / 3)
            + (ScaleTo(2, BattleScene.ZOOM_OUT_DURATION) | MoveTo((460, 370), BattleScene.ZOOM_OUT_DURATION))
        )
        self.add(self._pokemon)

        self.do(
            Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION)
            + CallFunc(self._start)
        )

    def _start(self) -> None:
        """Show the pokemon information."""

        self._opponent_hud = OpponentHUDLayer(self._opponent_pokemon)
        self._opponent_hud.position = (350, 370)
        self._opponent_hud.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._opponent_hud, z=50)

        self._hud = HUDLayer(self._players_pokemon)
        self._hud.position = (420, 180)
        self._hud.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._hud, z=50)

        self._dialog.do(FadeIn(0.5))

        self._actions = ActionsLayer()
        self._actions.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._actions)

        self._moves = MovesLayer(self._players_pokemon)
        self.add(self._moves)

        self.show_actions()

    def show_actions(self) -> None:
        """Ask the player to choose an action."""

        self._dialog.set_text(I18n().get("BATTLE.WHAT_WILL_DO").format(self._players_pokemon.nickname))

        self._actions.toggle_apparition()

    def show_moves(self) -> None:
        """Ask the player to choose a move for the pokemon."""

        self._moves.toggle_apparition()

    def fight_action(self, move: LearnedMoveModel) -> None:
        """The player selected a move. It is transmitted to the controller.

        :param move: The selected move.
        """

        self._moves.toggle_apparition()

        self._battle_controller.round(self._players_pokemon, self._opponent_pokemon,
                                      FightActionModel(self._players_pokemon, self._opponent_pokemon, move))

    def run_action(self) -> None:
        """The player selected to run. It is transmitted to the controller."""

        self._battle_controller.round(self._players_pokemon, self._opponent_pokemon,
                                      RunActionModel(self._players_pokemon, self._opponent_pokemon))

    def _successful_run(self) -> None:
        """The attempt to run is successful. The battle is over."""

        self._dialog.set_text(I18n().get("BATTLE.SUCCESSFUL_RUN"), lambda: self._battle_controller.run())

    def round(self, first_action: typing.Union[FightActionModel, RunActionModel],
              second_action: typing.Union[FightActionModel, RunActionModel]) -> None:
        """Play the actions.

        :param first_action: The first action.
        :param second_action: The second action.
        """

        self._do_action(first_action, second_action)

    def _do_action(self, action: typing.Union[FightActionModel, RunActionModel],
                   next_action: typing.Union[FightActionModel, RunActionModel] = None):
        """Perform the specified action.

        :param action: The action to play.
        :param next_action: The next action to be played.
        """

        callback = lambda: self._do_action(next_action) if next_action else self.show_actions()

        if isinstance(action, RunActionModel):
            if action.is_run_successful():
                self._successful_run()
            else:
                self._dialog.set_text(I18n().get("BATTLE.FAILED_RUN"), callback)
        elif isinstance(action, FightActionModel):
            self._dialog.set_text(
                I18n().get("BATTLE.MOVE_USED").format(action.attacker.nickname, action.move.move.name))
            if action.attacker == self._players_pokemon:
                self._pokemon.do(Delay(0.5) + MoveBy((15, 15), 0.10) + MoveBy((-15, -15), 0.10)
                                 + (CallFunc(self._opponent_hud.update_hp) | CallFunc(self._moves.update_moves)))
            else:
                self._opponent_pokemonLayer.do(Delay(0.5) + MoveBy((-15, -15), 0.10) + MoveBy((15, 15), 0.10)
                                               + CallFunc(self._hud.update_hp))

            delay = 1 if action.move.move.category == MoveCategoryEnum.STATUS else 2
            self._dialog.do(Delay(delay) + CallFunc(self._explain_fight_action_effects, action, callback))

    def _explain_fight_action_effects(self, action: FightActionModel, callback: typing.Callable) -> None:
        """Write the effects of the move to the user.

        :param action: The fight action being played.
        :param callback: The function to call after.
        """

        text = []
        effects = action.get_effects()

        if effects.failed:
            text.append(I18n().get("BATTLE.MOVE_FAILED").format(action.attacker.nickname))
        else:
            if effects.critical_hit:
                text.append(I18n().get("BATTLE.CRITICAL_HIT"))

            if effects.effectiveness and effects.effectiveness == MoveEffectivenessEnum.NO_EFFECT:
                text.append(I18n().get("BATTLE.NO_EFFECT"))
            elif effects.effectiveness and effects.effectiveness == MoveEffectivenessEnum.NOT_EFFECTIVE or effects.effectiveness == MoveEffectivenessEnum.VERY_INEFFECTIVE:
                text.append(I18n().get("BATTLE.NOT_EFFECTIVE"))
            elif effects.effectiveness and effects.effectiveness == MoveEffectivenessEnum.SUPER_EFFECTIVE or effects.effectiveness == MoveEffectivenessEnum.EXTREMELY_EFFECTIVE:
                text.append(I18n().get("BATTLE.SUPER_EFFECTIVE"))

            if action.defender.hp > 0:
                for staged_stat, stage in effects.staged_stats.items():
                    if stage > 0:
                        text.append(I18n().get("BATTLE.STAGED_STAT_{stage}".format(stage=stage)).format(
                            action.attacker.nickname, staged_stat.value[0]))
                    elif stage < 0:
                        text.append(I18n().get("BATTLE.STAGED_STAT_{stage}".format(stage=stage)).format(
                            action.defender.nickname, staged_stat.value[0]))

        if action.defender.hp > 0:
            if text:
                self._dialog.set_text(text, callback)
            else:
                callback()
        else:
            if text:
                self._dialog.set_text(text, lambda: self._pokemon_ko(action.defender))
            else:
                self._pokemon_ko(action.defender)

    def _pokemon_ko(self, pokemon: PokemonModel) -> None:
        """A pokemon is KO. Notify the user and the controller.

        :param pokemon: The pokemon who fainted.
        """

        if pokemon == self._players_pokemon:
            self._pokemon.do(MoveBy((-200, -200), 0.5))
        else:
            self._opponent_pokemonLayer.do(MoveBy((200, 0), 0.5))

        self._dialog.set_text(I18n().get("BATTLE.KO").format(pokemon.nickname),
                              lambda: self._battle_controller.pokemon_ko(pokemon, self._players_pokemon,
                                                                         self._opponent_pokemon))

    def player_won_fight(self, xp_points: int, gained_levels: typing.Dict[int, typing.Dict[StatEnum, int]]) -> None:
        """The player's pokemon defeated the opponent. They gain some XP.

        :param xp_points: The total number of gained xp points.
        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        self._dialog.set_text(I18n().get("BATTLE.GAINED_XP").format(self._players_pokemon.nickname, xp_points),
                              lambda: self.experience_gained(gained_levels))

    def experience_gained(self, gained_levels: typing.Dict[int, typing.Dict[StatEnum, int]]) -> None:
        """Update the XP bar.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        if len(gained_levels) > 0:
            self._hud.do(CallFunc(self._hud.update_xp, gained_levels[self._players_pokemon.level - len(gained_levels)])
                         + Delay(HUDLayer.XP_UPDATE_DURATION) + CallFunc(self._level_up, gained_levels))
        else:
            self._hud.do(CallFunc(self._hud.update_xp) +
                         Delay(HUDLayer.XP_UPDATE_DURATION + 0.5) + CallFunc(self._battle_controller.run))

    def _continue_experience_gained(self, gained_levels: typing.Dict[int, typing.Dict[StatEnum, int]]) -> None:
        """After leveling up, reset the XP bar and keep updating it.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        self._hud.reset_xp_bar()
        self._stats.kill()
        del gained_levels[self._players_pokemon.level - len(gained_levels)]
        self.experience_gained(gained_levels)

    def _level_up(self, gained_levels: typing.Dict[int, typing.Dict[StatEnum, int]]) -> None:
        """The pokemon has leveled up. Show a message to the player , the stat
        increase and a possible new move to learn.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        self._stats = StatLayer(self._players_pokemon, gained_levels)
        self._stats.position = (490, 70)
        self.add(self._stats, z=100)

        self._dialog.set_text(I18n().get("BATTLE.LEVEL_UP").format(self._players_pokemon.nickname,
                                                                   self._players_pokemon.level - (
                                                                           len(gained_levels) - 1)),
                              lambda: self._continue_experience_gained(gained_levels))
