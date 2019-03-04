import importlib
import random

import cocos
from cocos.actions import *

from toolbox.i18n import I18n
from views.common.dialog import Dialog
from .actions import Actions
from .background import Background
from .fade import Fade
from .hud import HUD
from .moves import Moves
from .opponent_hud import OpponentHUD
from .opponent_pokemon import OpponentPokemon
from .pokemon import Pokemon
from .transition import Transition


class BattleScene(cocos.scene.Scene):
    """The battle opposing two pokemon.

    Attributes:
        - BATTLE_TRANSITIONS: contains all of the transitions allowed between a
            scene and the battle scene.
        - TRANSITION_DURATION: How long the transition is visible in seconds.
        - TRAVELING_DURATION: How long the traveling on the opponent is.
        - TRANSITION_DURATION: How long the traveling from the opponent to the
            player's pokemon is.
    """

    BATTLE_TRANSITIONS = ["FadeTransition", "SplitColsTransition", "SplitRowsTransition", "FadeDownTransition",
                          "FadeUpTransition", "FadeBLTransition", "FadeTRTransition", "TurnOffTilesTransition"]
    TRANSITION_DURATION = 2
    TRAVELING_DURATION = 2
    ZOOM_OUT_DURATION = 1

    def __init__(self, players_pokemon, opponent_pokemon):
        super().__init__()

        self._players_pokemon = players_pokemon
        self._opponent_pokemon = opponent_pokemon

        transition_class = getattr(importlib.import_module("cocos.scenes.transitions"),
                                   random.choice(BattleScene.BATTLE_TRANSITIONS))
        cocos.director.director.replace(transition_class(self))

        self._intro()

    def _intro(self):
        """The "cinematic" showing the battle field and the pokemon."""

        self._transition = Transition()
        self._transition.do(
            Delay(BattleScene.TRANSITION_DURATION * 2 / 3) +
            (ScaleTo(3.5, BattleScene.TRANSITION_DURATION * 1 / 3) | FadeOut(BattleScene.TRANSITION_DURATION * 1 / 3)))
        self.add(self._transition, z=100)

        self._background = Background()
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
        self._dialog.text = I18n().get("BATTLE.WILD").format(self._opponent_pokemon.nickname)
        self.add(self._dialog, z=50)

        self._opponent_pokemonLayer = OpponentPokemon(self._opponent_pokemon)
        self._opponent_pokemonLayer.scale = 2
        self._opponent_pokemonLayer.position = (720, 400)
        self._opponent_pokemonLayer.do(Delay(BattleScene.TRANSITION_DURATION * 2 / 3)
                                       + MoveBy((250, 0), BattleScene.TRAVELING_DURATION)
                                       + MoveTo((720, 400), 0)
                                       + (ScaleTo(1, BattleScene.ZOOM_OUT_DURATION) | MoveBy((-180, -75),
                                                                                             BattleScene.ZOOM_OUT_DURATION))
                                       )
        self.add(self._opponent_pokemonLayer)

        self._fade = Fade()
        self._fade.do(Delay(BattleScene.TRANSITION_DURATION + BattleScene.TRAVELING_DURATION / 2)
                      + FadeIn(0.2)
                      + FadeOut(1)
                      )
        self.add(self._fade, z=100)

        self._pokemon = Pokemon(self._players_pokemon)
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

    def _start(self):
        """Show the pokemon information."""

        self._opponent_hud = OpponentHUD(self._opponent_pokemon)
        self._opponent_hud.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._opponent_hud, z=50)

        self._hud = HUD(self._players_pokemon)
        self._hud.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._hud, z=50)

        self._dialog.text = I18n().get("BATTLE.WHAT_WILL_DO").format(self._players_pokemon.nickname)
        self._dialog.do(FadeIn(0.5))

        self._actions = Actions()
        self._actions.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._actions)

        self._moves = Moves(self._players_pokemon)
        self.add(self._moves)

        self.show_actions()

    def show_actions(self):
        """Ask the player to choose an action."""

        self._actions.toggle_apparition()

    def fight_action(self):
        """Ask the player to choose a move for the pokemon."""

        self._moves.toggle_apparition()

    def move_selected(self, move):
        """The player selected a move. It is transmitted to the controller.

        :param move: The selected move
        """

        from controllers.battle import BattleController
        BattleController().uses_move(self._players_pokemon, self._opponent_pokemon, move)

    def round(self, first_attacker, second_attacker):
        self._moves.toggle_apparition()

        self._dialog.text = I18n().get("BATTLE.MOVE_USED").format(first_attacker["pokemon"].nickname,
                                                                  first_attacker["move"].move.name)
        if first_attacker["pokemon"] == self._players_pokemon:
            self._opponent_hud.update_hp()

        self._moves.update_moves()
