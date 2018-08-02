from types import SimpleNamespace
from random import choice

import pyxel

import reducer

class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.state = reducer.initial_state()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.word_complete:
            self.state = reducer.typo_reducer(
                self.state,
                reducer.SET_WORD,
                word=choice(self.state['all_words'])
            )
        else:
            for character, key in self.character_map.items():
                if self.state['current_word'][self.state['position']] == character and pyxel.btnp(key):
                    self.state = reducer.typo_reducer(self.state, reducer.TYPE_CHARACTER)
                    break

    @property
    def word_complete(self):
        return self.state['position'] == len(self.state['current_word'])

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

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, self.state['current_word'].upper(), 7)


if __name__ == '__main__':
    Game().run()
