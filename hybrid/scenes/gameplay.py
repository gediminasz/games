import pyxel

from pyxel_extensions import PALETTE
from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

import actions


NUCLEOBASE_WIDTH = 8
NUCLEOBASE_HEIGHT = NUCLEOBASE_WIDTH
NUCLEOBASE_PADDING = 1
NUCLEOBASE_ORDER = 'ACGT'
PADDING = 10
TOP_Y = 40
BOTTOM_Y = 50
OUTPUT_Y = 65


class GameplayScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            from .start import StartScene
            self.store.dispatch(actions.clear_puzzle())
            self.store.dispatch(change_scene(StartScene))

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.store.dispatch(actions.shift_left())
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.store.dispatch(actions.shift_right())
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.store.dispatch(actions.crossover())
        elif pyxel.btnp(pyxel.KEY_TAB):
            self.store.dispatch(actions.flip())

        if self.goal in (self.top_sequence, self.bottom_sequence):
            from .score import ScoreScene
            self.store.dispatch(change_scene(ScoreScene))

    def draw(self):
        pyxel.cls(1)
        pyxel.text(PADDING, PADDING, f'Goal: {self.goal}', PALETTE.WHITE)
        if 'description' in self.store.state['puzzle']:
            pyxel.text(PADDING, PADDING * 2, self.store.state['puzzle']['description'], PALETTE.BLUE)

        draw_crossover_highlight(self.crossover, len(self.top_sequence))

        draw_sequence(self.top_sequence, PADDING, TOP_Y, self.top_sequence == self.goal)
        draw_sequence(self.bottom_sequence, PADDING, BOTTOM_Y, self.bottom_sequence == self.goal)

    @property
    def top_sequence(self):
        return self.store.state['puzzle']['top']

    @property
    def bottom_sequence(self):
        return self.store.state['puzzle']['bottom']

    @property
    def goal(self):
        return self.store.state['puzzle']['goal']

    @property
    def output(self):
        return self.bottom_sequence[:self.crossover] + self.top_sequence[self.crossover:]

    @property
    def crossover(self):
        return self.store.state['puzzle']['crossover']


def draw_sequence(sequence, x, y, match):
    for i, nucleobase in enumerate(sequence):
        offset = i * (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING)
        draw_nucleobase(nucleobase, x + offset, y, match=match)


def draw_nucleobase(nucleobase, x, y, match=False):
    index = NUCLEOBASE_ORDER.index(nucleobase)
    source_x = index * NUCLEOBASE_WIDTH
    source_y = NUCLEOBASE_HEIGHT if match else 0
    pyxel.blt(x, y, 0, source_x, source_y, NUCLEOBASE_WIDTH, NUCLEOBASE_HEIGHT, PALETTE.BLACK)


def draw_crossover_highlight(crossover, sequence_length):
    pyxel.rect(
        PADDING + (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING) * crossover - 1,
        TOP_Y - 2,
        PADDING + (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING) * sequence_length - 1,
        TOP_Y + NUCLEOBASE_HEIGHT * 2 + 3,
        PALETTE.DARK_GREEN
    )
