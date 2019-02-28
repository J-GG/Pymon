import importlib
import random

import cocos
from cocos.actions import *

from toolbox.i18n import I18n
from views.common.dialog import Dialog
from .background import Background
from .fade import Fade
from .hud import HUD
from .opponent_hud import OpponentHUD
from .opponent_pokemon import OpponentPokemon
from .pokemon import Pokemon
from .transition import Transition


class FightScene(cocos.scene.Scene):
    """The fight opposing two pokemon.

    Attributes:
        - FIGHT_TRANSITIONS: contains all of the transitions allowed between a
            scene and the fight scene.
        - TRANSITION_DURATION: How long the transition is visible in seconds.
        - TRAVELING_DURATION: How long the traveling on the opponent is.
        - TRANSITION_DURATION: How long the traveling from the opponent to the
            player's pokemon is.
    """

    FIGHT_TRANSITIONS = ["FadeTransition", "SplitColsTransition", "SplitRowsTransition", "FadeDownTransition",
                         "FadeUpTransition", "FadeBLTransition", "FadeTRTransition", "TurnOffTilesTransition"]
    TRANSITION_DURATION = 2
    TRAVELING_DURATION = 2
    ZOOM_OUT_DURATION = 1

    def __init__(self):
        super(FightScene, self).__init__()

        transition_class = getattr(importlib.import_module("cocos.scenes.transitions"),
                                   random.choice(FightScene.FIGHT_TRANSITIONS))
        cocos.director.director.replace(transition_class(self))

        self._intro()

    def _intro(self):
        """The "cinematic" showing the battle field and the pokemon."""

        self._transition = Transition()
        self._transition.do(
            Delay(FightScene.TRANSITION_DURATION * 2 / 3) +
            (ScaleTo(3.5, FightScene.TRANSITION_DURATION * 1 / 3) | FadeOut(FightScene.TRANSITION_DURATION * 1 / 3)))
        self.add(self._transition, z=100)

        self._background = Background()
        self._background.scale = 2
        self._background.position = (160, 240)
        self._background.do(Delay(FightScene.TRANSITION_DURATION * 2 / 3)
                            + MoveBy((250, 0), FightScene.TRAVELING_DURATION)
                            + MoveTo((160, 240), 0)
                            + (ScaleTo(1, FightScene.ZOOM_OUT_DURATION)
                               | MoveTo((260, 240), FightScene.ZOOM_OUT_DURATION))
                            )
        self.add(self._background)

        self._dialog = Dialog()
        self._dialog.do(Delay(FightScene.TRANSITION_DURATION + FightScene.TRAVELING_DURATION / 2 + 0.2)
                        + FadeOut(0)
                        + Delay(FightScene.ZOOM_OUT_DURATION - 0.2)
                        )
        self._dialog.text = I18n().get("FIGHT.WILD").format("Bulbasaur")
        self.add(self._dialog, z=50)

        self._opponent_pokemon = OpponentPokemon()
        self._opponent_pokemon.scale = 2
        self._opponent_pokemon.position = (720, 400)
        self._opponent_pokemon.do(Delay(FightScene.TRANSITION_DURATION * 2 / 3)
                                  + MoveBy((250, 0), FightScene.TRAVELING_DURATION)
                                  + MoveTo((720, 400), 0)
                                  + (ScaleTo(1, FightScene.ZOOM_OUT_DURATION) | MoveBy((-180, -75),
                                                                                       FightScene.ZOOM_OUT_DURATION))
                                  )
        self.add(self._opponent_pokemon)

        self._fade = Fade()
        self._fade.do(Delay(FightScene.TRANSITION_DURATION + FightScene.TRAVELING_DURATION / 2)
                      + FadeIn(0.2)
                      + FadeOut(1)
                      )
        self.add(self._fade, z=100)

        self._pokemon = Pokemon()
        self._pokemon.scale = 2.5
        self._pokemon.position = (150, 150)
        self._pokemon.do(
            Delay(FightScene.TRANSITION_DURATION + FightScene.TRAVELING_DURATION * 2 / 3)
            + (ScaleTo(2, FightScene.ZOOM_OUT_DURATION) | MoveTo((460, 370), FightScene.ZOOM_OUT_DURATION))
        )
        self.add(self._pokemon)

        self.do(
            Delay(FightScene.TRANSITION_DURATION + FightScene.TRAVELING_DURATION)
            + CallFunc(self._start)
        )

    def _start(self):
        """Show the pokemon information and let the player choose an action."""

        self._opponent_hud = OpponentHUD()
        self._opponent_hud.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._opponent_hud, z=50)

        self._hud = HUD()
        self._hud.do(FadeOut(0) + FadeIn(0.5))
        self.add(self._hud, z=50)
