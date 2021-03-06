import pyxel

from pyxel_extensions import change_scene, PALETTE, Scene

from .gameplay import GameplayScene


class ScoreScene(GameplayScene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            from .puzzle_select import PuzzleSelectScene
            self.store.dispatch(change_scene(PuzzleSelectScene))

    def draw(self):
        super().draw()
        pyxel.rect(63, 38, 96, 46, PALETTE.BLACK)
        pyxel.text(65, 40, 'Success!', PALETTE.GREEN)
        pyxel.rect(23, 58, 136, 66, PALETTE.BLACK)
        pyxel.text(25, 60, 'Press <space> to play again.', PALETTE.GRAY)
