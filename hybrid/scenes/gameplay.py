import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene


class GameplayScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            from .start import StartScene
            self.store.dispatch(change_scene(StartScene))

    def draw(self):
        pyxel.text(10, 10, 'GameplayScene', 7)
