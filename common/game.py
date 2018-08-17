import pyxel

from .store import Store


class Game:
    def __init__(self, initial_state, reducer):
        self.init_pyxel()

        self.store = Store(initial_state, reducer)

    def init_pyxel(self):
        pyxel.init(160, 120)
