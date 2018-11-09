import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

from actions import clear_puzzle, shift_left, shift_right, crossover
from .score import ScoreScene


NUCLEOBASE_WIDTH = 8
NUCLEOBASE_HEIGHT = NUCLEOBASE_WIDTH
NUCLEOBASE_PADDING = 1
NUCLEOBASE_ORDER = 'ACGT'


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

        if self.goal in (self.top_sequence, self.bottom_sequence):
            self.store.dispatch(change_scene(ScoreScene))

    def draw(self):
        pyxel.text(10, 10, f'Goal: {self.goal}', 7)

        draw_sequence(self.top_sequence, 10, 40)
        draw_sequence(self.bottom_sequence, 10, 50)
        draw_output(self.output, self.goal, 10, 65)

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
        cut_index = len(self.top_sequence) // 2
        return self.bottom_sequence[:cut_index] + self.top_sequence[cut_index:]


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
    pyxel.blt(x, y, 0, source_x, source_y, NUCLEOBASE_WIDTH, NUCLEOBASE_HEIGHT)
