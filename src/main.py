import cocos

from controllers.intro import IntroController
from toolbox.init import init_pyglet

if __name__ == '__main__':
    init_pyglet()

    cocos.director.director.init(caption="Pymon")
    IntroController.show_intro()
