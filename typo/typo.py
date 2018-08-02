from types import SimpleNamespace
from random import choice

import pyxel

class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.state = SimpleNamespace(
            all_words=self.load_words('words.txt'),
            remaining_input='',
            words_typed=1
        )

    def load_words(self, source):
        with open(source, 'r') as f:
            return f.read().split()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state.remaining_input:
            for character, key in self.character_map.items():
                if self.state.remaining_input[0] == character and pyxel.btnp(key):
                    self.state.remaining_input = self.state.remaining_input[1:]
                    break

        else:
            self.state.words_typed += 1
            self.state.remaining_input = choice(self.state.all_words)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, str(self.state.remaining_input), 7)

    @property
    def character_map(self):
        return {
            'a': pyxel.KEY_A,
            'b': pyxel.KEY_B,
            'c': pyxel.KEY_C,
            'd': pyxel.KEY_D,
            'e': pyxel.KEY_E,
            'f': pyxel.KEY_F,
            'g': pyxel.KEY_G,
            'h': pyxel.KEY_H,
            'i': pyxel.KEY_I,
            'j': pyxel.KEY_J,
            'k': pyxel.KEY_K,
            'l': pyxel.KEY_L,
            'm': pyxel.KEY_M,
            'n': pyxel.KEY_N,
            'o': pyxel.KEY_O,
            'p': pyxel.KEY_P,
            'q': pyxel.KEY_Q,
            'r': pyxel.KEY_R,
            's': pyxel.KEY_S,
            't': pyxel.KEY_T,
            'u': pyxel.KEY_U,
            'v': pyxel.KEY_V,
            'w': pyxel.KEY_W,
            'x': pyxel.KEY_X,
            'y': pyxel.KEY_Y,
            'z': pyxel.KEY_Z,
        }


if __name__ == '__main__':
    Game().run()
