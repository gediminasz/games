import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

from actions import clear_puzzle, shift_left, shift_right, crossover
from .score import ScoreScene


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

        self.draw_sequence(self.top_sequence, 10, 40)
        self.draw_sequence(self.bottom_sequence, 10, 50)
        self.draw_output(10, 65)

    def draw_sequence(self, sequence, x, y):
        for i, nucleobase in enumerate(sequence):
            self.draw_nucleobase(nucleobase, x + i * 9, y)

    def draw_output(self, x, y):
        for i, nucleobase in enumerate(self.output):
            match = nucleobase == self.goal[i]
            self.draw_nucleobase(nucleobase, x + i * 9, y, match)

    def draw_nucleobase(self, nucleobase, x, y, match=False):
        nucleobase_indexes = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        offset = nucleobase_indexes[nucleobase] * 8
        vertical_offset = 8 if match else 0
        pyxel.blt(x, y, 0, offset, vertical_offset, 8, 8)

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
