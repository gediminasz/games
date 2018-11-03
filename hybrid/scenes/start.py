import pyxel

from pyxel_extensions.scene import Scene


class StartScene(Scene):
    def update(self):
        pass

    def draw(self):
        pyxel.text(55, 40, 'H Y B R I D', 3)
