import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

from .gameplay import GameplayScene


class ScoreScene(GameplayScene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            from .puzzle_select import PuzzleSelectScene
            self.store.dispatch(change_scene(PuzzleSelectScene))

    def draw(self):
        super().draw()
        pyxel.text(65, 40, 'Success!', 11)
        pyxel.text(25, 60, 'Press <space> to play again.', 6)
