import pyxel

from pyxel_extensions import PALETTE
from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene


class StartScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            from .puzzle_select import PuzzleSelectScene
            self.store.dispatch(change_scene(PuzzleSelectScene))

    def draw(self):
        pyxel.text(56, 40, 'H Y B R I D', PALETTE.BROWN)
        pyxel.text(55, 41, 'H Y B R I D', PALETTE.BROWN)
        pyxel.text(56, 41, 'H Y B R I D', PALETTE.BROWN)
        pyxel.text(55, 40, 'H Y B R I D', PALETTE.ORANGE)

        pyxel.text(35, 60, 'Press <space> to start', PALETTE.GRAY)
