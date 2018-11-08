import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene



class ScoreScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            from .start import StartScene
            self.store.dispatch(change_scene(StartScene))

    def draw(self):
        pyxel.text(65, 40, 'Success!', 11)
        pyxel.text(25, 60, 'Press <space> to play again.', 6)
