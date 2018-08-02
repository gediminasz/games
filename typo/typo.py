from types import SimpleNamespace
from random import choice

import pyxel

from reducer import (
    END_GAME,
    initial_state,
    NEXT_WORD,
    SCENE_GAME,
    SCENE_START,
    START_GAME,
    TYPE_CHARACTER,
    typo_reducer,
)


WORD_COUNT = 5


class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.state = initial_state()

    def dispatch(self, action_type, **kwargs):
        self.state = typo_reducer(self.state, action_type, **kwargs)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state['current_scene'] == SCENE_START:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.dispatch(START_GAME)

        if self.state['current_scene'] == SCENE_GAME:
            if self.word_complete:
                if self.state['count'] == WORD_COUNT:
                    self.dispatch(END_GAME)
                else:
                    self.dispatch(NEXT_WORD, word=choice(self.state['all_words']))
            else:
                for character, key in self.character_map.items():
                    if character == self.current_character and pyxel.btnp(key):
                        self.dispatch(TYPE_CHARACTER)
                        break

    @property
    def word_complete(self):
        return self.state['position'] == len(self.state['current_word'])

    @property
    def current_character(self):
        return self.state['current_word'][self.state['position']]

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

        if self.state['current_scene'] == SCENE_START:
            pyxel.text(70, 40, 'TYPO', 3)
            pyxel.text(35, 60, 'Press <space> to start', 7)

        elif self.state['current_scene'] == SCENE_GAME:
            current_word = self.state['current_word'].upper()
            pyxel.text(10, 10, current_word, 7)
            pyxel.text(10, 10, current_word[:self.state['position']], 5)


if __name__ == '__main__':
    Game().run()
