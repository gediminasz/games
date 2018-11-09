import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

from actions import clear_puzzle, shift_left, shift_right, crossover, flip
from .score import ScoreScene


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
            self.store.dispatch(clear_puzzle())
            self.store.dispatch(change_scene(StartScene))

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.store.dispatch(shift_left())
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.store.dispatch(shift_right())
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.store.dispatch(crossover())
        elif pyxel.btnp(pyxel.KEY_TAB):
            self.store.dispatch(flip())

        if self.goal in (self.top_sequence, self.bottom_sequence):
            self.store.dispatch(change_scene(ScoreScene))

    def draw(self):
        pyxel.cls(1)
        pyxel.text(PADDING, PADDING, f'Goal: {self.goal}', 7)

        draw_crossover_highlight(self.crossover_point, len(self.top_sequence))

        draw_sequence(self.top_sequence, PADDING, TOP_Y)
        draw_sequence(self.bottom_sequence, PADDING, BOTTOM_Y)
        draw_output(self.output, self.goal, PADDING, OUTPUT_Y)

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
        return self.bottom_sequence[:self.crossover_point] + self.top_sequence[self.crossover_point:]

    @property
    def crossover_point(self):
        return self.store.state['puzzle']['crossover_point']

def draw_sequence(sequence, x, y):
    for i, nucleobase in enumerate(sequence):
        offset = i * (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING)
        draw_nucleobase(nucleobase, x + offset, y)


def draw_output(sequence, goal, x, y):
    for i, nucleobase in enumerate(sequence):
        offset = i * (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING)
        match = nucleobase == goal[i]
        draw_nucleobase(nucleobase, x + offset, y, match)


def draw_nucleobase(nucleobase, x, y, match=False):
    index = NUCLEOBASE_ORDER.index(nucleobase)
    source_x = index * NUCLEOBASE_WIDTH
    source_y = NUCLEOBASE_HEIGHT if match else 0
    pyxel.blt(x, y, 0, source_x, source_y, NUCLEOBASE_WIDTH, NUCLEOBASE_HEIGHT, 0)


def draw_crossover_highlight(crossover_point, sequence_length):
    pyxel.rect(
        PADDING + (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING) * crossover_point - 1,
        TOP_Y - 2,
        PADDING + (NUCLEOBASE_WIDTH + NUCLEOBASE_PADDING) * sequence_length - 1,
        OUTPUT_Y + NUCLEOBASE_HEIGHT + 1,
        3
    )
