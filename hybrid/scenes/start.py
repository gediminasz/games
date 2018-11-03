import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

from .gameplay import GameplayScene


class StartScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.store.dispatch(change_scene(GameplayScene))

    def draw(self):
        pyxel.text(55, 40, 'H Y B R I D', 3)
