import importlib
import random
import typing

import cocos
from cocos.actions import *

from models.battle.battle_model import BattleModel
from models.battle.fight_action_model import FightActionModel
from models.battle.run_action_model import RunActionModel
from models.battle.shift_action_model import ShiftActionModel
from models.enumerations.move_category_enum import MoveCategoryEnum
from models.enumerations.move_effectiveness_enum import MoveEffectivenessEnum
from models.learned_move_model import LearnedMoveModel
from models.move_model import MoveModel
from models.pokemon_model import PokemonModel
from toolbox.game import Game
from toolbox.i18n import I18n
from views.common.dialog import Dialog
from views.common.stat_layer import StatLayer
from views.pkmn_infos.pkmn_infos_type_enum import PkmnInfosTypeEnum
from .actions_layer import ActionsLayer
from .background_layer import BackgroundLayer
from .fade_layer import FadeLayer
from .go_pokemon_layer import GoPokemonLayer
from .hud_layer import HUDLayer
from .moves_layer import MovesLayer
from .opponent_hud_layer import OpponentHUDLayer
from .opponent_pokemon_layer import OpponentPokemonLayer
from .pokemon_layer import PokemonLayer
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

    def __init__(self, battle_controller, battle: BattleModel) -> None:
        """Create a battle scene.

        :param battle_controller: The controller to be called to manage.
        :param battle: The data of the battle.
        """

        super().__init__()
        self._battle_controller = battle_controller
        self._battle = battle

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
                        + FadeOut(0))
        self._dialog.set_text(I18n().get("BATTLE.WILD").format(self._battle.opponent_pokemon.nickname))
        self.add(self._dialog, z=75)

        self._opponent_pokemonLayer = OpponentPokemonLayer(self._battle.opponent_pokemon)
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

        self._opponent_hud = OpponentHUDLayer(self._battle.opponent_pokemon)
        self._opponent_hud.position = (350, 370)
        self._opponent_hud.opacity = 0
        self._opponent_hud.do(Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION)
                              + FadeIn(0.5))
        self.add(self._opponent_hud, z=50)

        self._actions = ActionsLayer()
        self.add(self._actions)

        self._moves = MovesLayer(self._battle.players_pokemon)
        self.add(self._moves)

        self._go_pokemon = GoPokemonLayer()
        self.add(self._go_pokemon, z=60)

        self._hud = None
        self._pokemon = None
        self._add_pkmn()
        self._pokemon.opacity = 0
        self._hud.opacity = 0

        self.do(
            Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION)
            + CallFunc(self._send_pokemon)
        )

    def _add_pkmn(self, forced_hp: int = None) -> None:
        """Add the pokemon layer and the HUD layer.

        The ``forced_hp`` parameter is only useful if the current number of HP is
        different from the displayed one.

        :param forced_hp: The number of HP to display.
        """

        if self._pokemon:
            self.remove(self._pokemon)

        self._pokemon = PokemonLayer(self._battle.players_pokemon)
        self._pokemon.scale = 2
        self._pokemon.position = (450, 350)
        self.add(self._pokemon)

        if self._hud:
            self.remove(self._hud)

        self._hud = HUDLayer(self._battle.players_pokemon, forced_hp)
        self._hud.position = (420, 180)
        self.add(self._hud, z=50)

    def _send_pokemon(self) -> None:
        """Show the player's pokemon."""

        self._go_pokemon.animation()

        self._dialog.set_text("")
        self._dialog.do(FadeIn(0.4) |
                        (Delay(0.2) + CallFunc(self._dialog.set_text,
                                               I18n().get("BATTLE.GO_POKEMON").format(
                                                   self._battle.players_pokemon.nickname))))

        self._pokemon.do(Delay(1.6) + FadeIn(0.5))
        self._hud.do(Delay(2) + FadeIn(0.5))

        self.do(Delay(2.2) + CallFunc(self.show_actions))

    def show_actions(self) -> None:
        """Ask the player to choose an action."""

        self._dialog.set_text(I18n().get("BATTLE.WHAT_WILL_DO").format(self._battle.players_pokemon.nickname))

        self._actions.toggle_apparition()

    def show_moves(self) -> None:
        """Ask the player to choose a move for the pokemon."""

        self._moves.toggle_apparition()

    def fight_action(self, move: LearnedMoveModel) -> None:
        """The player selected a move. It is transmitted to the controller.

        :param move: The selected move.
        """

        self._moves.toggle_apparition()

        self._battle_controller.round(
            FightActionModel(self._battle, True, move))

    def run_action(self) -> None:
        """The player selected to run. It is transmitted to the controller."""

        self._battle_controller.round(RunActionModel(self._battle.players_pokemon, self._battle.opponent_pokemon))

    def _successful_run(self) -> None:
        """The attempt to run is successful. The battle is over."""

        self._dialog.set_text(I18n().get("BATTLE.SUCCESSFUL_RUN"), lambda: self._battle_controller.run())

    def round(self, first_action: typing.Union[FightActionModel, RunActionModel, ShiftActionModel],
              second_action: typing.Union[FightActionModel, RunActionModel, ShiftActionModel]) -> None:
        """Play the actions.

        :param first_action: The first action.
        :param second_action: The second action.
        """

        self._do_action(first_action, second_action)

    def _do_action(self, action: typing.Union[FightActionModel, RunActionModel, ShiftActionModel],
                   next_action: typing.Union[FightActionModel, RunActionModel, ShiftActionModel] = None):
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
        elif isinstance(action, ShiftActionModel):
            hp = action.pokemon.hp - next_action.get_effects().hp if isinstance(next_action,
                                                                                FightActionModel) else None

            self._actions.do(CallFunc(self._actions.toggle_apparition))
            self._go_pokemon.flash(True)
            self._dialog.set_text(I18n().get("BATTLE.COME_BACK").format(action.previous_pokemon.nickname))
            self._pokemon.do(Delay(1.5) + CallFunc(self._add_pkmn, hp))
            self._dialog.do(Delay(1.5)
                            + CallFunc(self._dialog.set_text,
                                       I18n().get("BATTLE.GO_POKEMON").format(action.pokemon.nickname)))

            self.remove(self._moves)
            self._moves = MovesLayer(action.pokemon)
            self.add(self._moves)

            self.do(Delay(3) + CallFunc(callback))
        elif isinstance(action, FightActionModel):
            self._dialog.set_text(
                I18n().get("BATTLE.MOVE_USED").format(action.attacker.nickname, action.move.move.name))
            if action.attacker == self._battle.players_pokemon:
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
                    if stage > 0 or stage < 0:
                        if stage > 0:
                            pokemon_name = action.attacker.nickname
                        else:
                            pokemon_name = action.defender.nickname
                        text.append(I18n().get("BATTLE.STAGED_STAT_{0}".format(stage)).format(pokemon_name, I18n().get(
                            "STAT.{0}".format(staged_stat.name))))

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

        if pokemon == self._battle.players_pokemon:
            self._pokemon.do(MoveBy((-200, -200), 0.5))
        else:
            self._opponent_pokemonLayer.do(MoveBy((200, 0), 0.5))

        self._dialog.set_text(I18n().get("BATTLE.KO").format(pokemon.nickname),
                              lambda: self._battle_controller.pokemon_ko(pokemon))

    def player_won_fight(self, xp_points: int, gained_levels: typing.Dict[int, typing.Dict]) -> None:
        """The player's pokemon defeated the opponent. They gain some XP.

        :param xp_points: The total number of gained xp points.
        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        self._dialog.set_text(I18n().get("BATTLE.GAINED_XP").format(self._battle.players_pokemon.nickname, xp_points),
                              lambda: self.experience_gained(gained_levels))

    def experience_gained(self, gained_levels: typing.Dict[int, typing.Dict]) -> None:
        """Update the XP bar.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        if len(gained_levels) > 0:
            self._hud.do(CallFunc(self._hud.update_xp, next(iter(gained_levels.values())))
                         + Delay(HUDLayer.XP_UPDATE_DURATION)
                         + CallFunc(self._level_up, gained_levels))
        else:
            self._hud.do(CallFunc(self._hud.update_xp)
                         + Delay(HUDLayer.XP_UPDATE_DURATION + 0.5)
                         + CallFunc(self._battle_controller.won_battle))

    def _level_up(self, gained_levels: typing.Dict[int, typing.Dict]) -> None:
        """The pokemon has leveled up. Show a message to the player , the stat
        increase and a possible new move to learn.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        self._stats = StatLayer(self._battle.players_pokemon, gained_levels)
        self._stats.position = (490, 70)
        self.add(self._stats, z=100)

        self._dialog.set_text(I18n().get("BATTLE.LEVEL_UP").format(self._battle.players_pokemon.nickname,
                                                                   next(iter(gained_levels.keys()))),
                              lambda: self._continue_experience_gained(gained_levels))

    def _continue_experience_gained(self, gained_levels: typing.Dict[int, typing.Dict]) -> None:
        """After leveling up, remove the stat increase panel.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level.
        """

        if self._stats:
            self._stats.kill()
            self._stats = None
        self._hud.reset_xp_bar()

        if next(iter(gained_levels.values()))["moves"]:
            self._new_move_to_learn(gained_levels)
        else:
            del gained_levels[next(iter(gained_levels.keys()))]
            self.experience_gained(gained_levels)

    def _new_move_to_learn(self, gained_levels: typing.Dict[int, typing.Dict]) -> None:
        """After leveling up, suggest the player to learn new moves.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level and the new moves.
        """

        new_move = next(iter(gained_levels.values()))["moves"][0]
        del gained_levels[next(iter(gained_levels.keys()))]["moves"][0]

        just_learned = False
        for learnedMove in self._battle.players_pokemon.moves:
            if learnedMove.move == new_move:
                just_learned = True
                break

        if just_learned:
            self.learn_move(gained_levels, new_move)
        else:
            self._dialog.set_text(
                [I18n().get("BATTLE.WANTS_NEW_MOVE").format(self._battle.players_pokemon.nickname, new_move.name),
                 I18n().get("BATTLE.TOO_MANY_MOVES").format(self._battle.players_pokemon.nickname),
                 I18n().get("BATTLE.SHOULD_FORGET_MOVE").format(new_move.name)],
                lambda answer: self._confirmation_not_learn_move(gained_levels,
                                                                 new_move) if answer == 1 else self._show_infos_new_move(
                    gained_levels,
                    new_move),
                choices=[I18n().get("COMMON.YES"), I18n().get("COMMON.NO")])

    def learn_move(self, gained_levels: typing.Dict[int, typing.Dict], new_move: MoveModel,
                   forgot_move: LearnedMoveModel = None):
        """The pokemon learned a new move.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level and the new moves.
        :param new_move: The move the player chose not to learn.
        :param forgot_move: The ``LearnedMoveModel`` the player decided
        """

        if forgot_move:
            self._dialog.set_text(
                I18n().get("BATTLE.REPLACE_MOVE").format(self._battle.players_pokemon.nickname, forgot_move.move.name,
                                                         new_move.name),
                lambda: self._continue_experience_gained(gained_levels))
        else:
            self._dialog.set_text(
                I18n().get("BATTLE.MOVE_LEARNED").format(self._battle.players_pokemon.nickname, new_move.name),
                lambda: self._continue_experience_gained(gained_levels))

    def _didnt_learn_move(self, gained_levels: typing.Dict[int, typing.Dict], new_move: MoveModel) -> None:
        """After leveling up, the player didn't want to learn the new move.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level and the new moves.
        :param new_move: The move the player chose not to learn.
        """

        self._dialog.set_text(
            I18n().get("BATTLE.DIDNT_LEARN_MOVE").format(self._battle.players_pokemon.nickname, new_move.name),
            lambda: self._continue_experience_gained(gained_levels))

    def _show_infos_new_move(self, gained_levels: typing.Dict[int, typing.Dict], new_move: MoveModel) -> None:
        """The players wants to learn the new move. Show the PKMN infos scene
        to choose which move to forget.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level and the new moves.
        :param new_move: The new move to learn.
        """

        self._battle_controller.infos_pkmn(PkmnInfosTypeEnum.NEW_MOVE, new_move=new_move,
                                           cancel_callback=lambda move_to_forget=None: self._result_infos_new_move(
                                               gained_levels,
                                               new_move, move_to_forget))

    def _confirmation_not_learn_move(self, gained_levels: typing.Dict[int, typing.Dict], new_move: MoveModel) -> None:
        """Ask the player to confirm he doesn't want to learn the new move.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level and the new moves.
        :param new_move: The new ``MoveModel`` to learn.
        """

        self._dialog.set_text(
            I18n().get("BATTLE.CONFIRMATION_NOT_LEARN_MOVE").format(new_move.name),
            lambda answer: self._didnt_learn_move(gained_levels,
                                                  new_move) if answer == 0 else self._show_infos_new_move(gained_levels,
                                                                                                          new_move),
            choices=[I18n().get("COMMON.YES"), I18n().get("COMMON.NO")])

    def _result_infos_new_move(self, gained_levels: typing.Dict[int, typing.Dict], new_move: MoveModel,
                               move_to_forget: [LearnedMoveModel]) -> None:
        """Ask the player to confirm he doesn't want to learn the new move.

        :param gained_levels: A dictionary with the gained levels as well as
        the stats increase for each level and the new moves.
        :param new_move: The new ``MoveModel`` to learn.
        :param move_to_forget: The ``LearnedMoveModel`` the player wants to
        forget or None if he doesn't want.
        """

        if not move_to_forget:
            self._confirmation_not_learn_move(gained_levels, new_move)
        else:
            move = move_to_forget[0]
            self._dialog.set_text(I18n().get("BATTLE.FORGET_MOVE").format(move.move.name, new_move.name),
                                  callback=lambda answer: self._battle_controller.forget_move(gained_levels,
                                                                                              new_move,
                                                                                              move) if answer == 0 else self._show_infos_new_move(
                                      gained_levels,
                                      new_move),
                                  choices=[I18n().get("COMMON.YES"), I18n().get("COMMON.NO")])

    def player_lost_battle(self) -> None:
        """The player lost the battle. Display a message."""

        self._dialog.set_text([I18n().get("BATTLE.OUT_OF_POKEMON").format(Game().game_state.player.name),
                               I18n().get("BATTLE.WHITED_OUT").format(Game().game_state.player.name)],
                              self._battle_controller.lost_battle)

    def ask_player_shift_pokemon(self) -> None:
        """The player's pokemon fainted. Ask him if he wants to shift."""

        self._dialog.set_text([I18n().get("BATTLE.USE_NEXT")],
                              callback=lambda
                                  choice: self.show_infos_shift_pokemon_out() if choice == 0 else self._successful_run(),
                              choices=[I18n().get("COMMON.YES"), I18n().get("COMMON.NO")])

    def show_infos_shift_pokemon_out(self) -> None:
        """Show the PKMN information scene to let the player choose a new
        PKMN to send after his pokemon got defeated."""

        self._battle_controller.infos_pkmn(PkmnInfosTypeEnum.SHIFT_POKEMON_OUT,
                                           cancel_callback=self.ask_player_shift_pokemon)

    def show_infos(self) -> None:
        """Show the PKMN information scene."""

        self._battle_controller.infos_pkmn(PkmnInfosTypeEnum.SHIFT)

    def shift_players_pokemon(self, action: ShiftActionModel) -> None:
        """Shift the player's pokemon

        :param action: The ``ShiftActionModel``.
        """

        self._go_pokemon.flash()
        self._pokemon.do(Delay(1.5) + CallFunc(self._add_pkmn))
        self._dialog.set_text(I18n().get("BATTLE.GO_POKEMON").format(action.pokemon.nickname))

        self.remove(self._moves)
        self._moves = MovesLayer(action.pokemon)
        self.add(self._moves)

        self.do(Delay(2) + CallFunc(self.show_actions))
