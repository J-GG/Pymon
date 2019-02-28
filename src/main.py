import os

import cocos
import pyglet

from controllers.main_menu import MainMenuController

if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.realpath(__file__))
    pyglet.resource.path = [os.path.join(working_dir, '../assets')]
    pyglet.resource.reindex()

    cocos.director.director.init()

    MainMenuController().show_menu()
