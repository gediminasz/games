import pyxel

from pyxel_extensions.scene import Scene
from pyxel_extensions.actions import change_scene

from actions import clear_puzzle


class GameplayScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            from .start import StartScene
            self.store.dispatch(clear_puzzle())
            self.store.dispatch(change_scene(StartScene))

    def draw(self):
        pyxel.text(10, 10, f'Goal: {self.goal}', 12)

        pyxel.text(10, 30, self.top_sequence, 7)
        pyxel.text(10, 40, self.bottom_sequence, 7)
        pyxel.text(10, 50, self.output, 8)

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
        assert len(self.top_sequence) == len(self.bottom_sequence)
        cut_index = len(self.top_sequence) // 2
        return self.bottom_sequence[:cut_index] + self.top_sequence[cut_index:]
