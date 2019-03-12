import os

import pyglet

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


def init_pyglet() -> None:
    """Initialize the resource folder used by pyglet."""

    pyglet.resource.path = [PATH + '/assets']
    pyglet.resource.reindex()


def init_game() -> None:
    """Initialize the game"""
