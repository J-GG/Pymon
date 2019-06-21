import cocos

from controllers.intro_controller import IntroController

if __name__ == '__main__':
    cocos.director.director.init(caption="Pymon", width=640, height=480, autoscale=True, resizable=True)
    IntroController.show_intro()
