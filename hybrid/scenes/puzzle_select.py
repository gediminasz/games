import pyxel

from pyxel_extensions import change_scene, PALETTE, Scene

from actions import load_puzzle, select_puzzle

SELECT_PREVIOUS = -1
SELECT_NEXT = +1
PADDING = 10


class PuzzleSelectScene(Scene):
    def update(self):

        if pyxel.btnp(pyxel.KEY_SPACE):
            puzzle = self.store.state['puzzles'][self.selected_puzzle]
            self.store.dispatch(load_puzzle(puzzle))

            from .gameplay import GameplayScene
            self.store.dispatch(change_scene(GameplayScene))

        elif pyxel.btnp(pyxel.KEY_UP):
            self.select_puzzle(SELECT_PREVIOUS)

        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.select_puzzle(SELECT_NEXT)

    def draw(self):
        for i, puzzle in enumerate(self.store.state['puzzles']):
            indicator = '>' if self.selected_puzzle == i else ' '
            label = f"{indicator}[{i:02}] {puzzle['top']} {puzzle['bottom']} -> {puzzle['goal']}"
            pyxel.text(PADDING, (i + 1) * PADDING, label, PALETTE.WHITE)

    @property
    def selected_puzzle(self):
        return self.store.state['puzzle_select']['selected_puzzle']

    def select_puzzle(self, delta):
        index = (self.selected_puzzle + delta) % len(self.store.state['puzzles'])
        self.store.dispatch(select_puzzle(index))
