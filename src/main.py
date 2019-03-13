import cocos

from controllers.intro_controller import IntroController

if __name__ == '__main__':
    cocos.director.director.init(caption="Pymon")
    IntroController.show_intro()
