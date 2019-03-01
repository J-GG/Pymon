import os

import cocos
import pyglet

from controllers.intro import IntroController

if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.realpath(__file__))
    pyglet.resource.path = [os.path.join(working_dir, '../assets/img')]
    pyglet.resource.reindex()

    cocos.director.director.init(caption="Pymon")

    IntroController.show_itro()
