import cocos

from controllers.intro import IntroController
from toolbox.data.pokemon import pokemons
from toolbox.init import init_pyglet

if __name__ == '__main__':
    init_pyglet()

    cocos.director.director.init(caption="Pymon")
    print(pokemons)
    IntroController.show_itro()
