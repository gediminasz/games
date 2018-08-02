from random import choice
import time

import pyxel

from reducer import initial_state, typo_reducer
import actions
import constants


class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.state = initial_state()

    def dispatch(self, action_type, **kwargs):
        self.state = typo_reducer(self.state, action_type, **kwargs)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state['current_scene'] == constants.SCENE_START:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.dispatch(actions.START_GAME, time=time.time())

        if self.state['current_scene'] == constants.SCENE_GAME:
            if self.word_complete:
                if self.state['count'] == constants.WORD_COUNT:
                    self.dispatch(actions.END_GAME, time=time.time())
                else:
                    self.dispatch(actions.NEXT_WORD, word=choice(self.state['all_words']))
            else:
                for character, key in self.character_map.items():
                    if character == self.current_character and pyxel.btnp(key):
                        self.dispatch(actions.TYPE_CHARACTER)
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

        if self.state['current_scene'] == constants.SCENE_START:
            pyxel.text(70, 40, 'TYPO', 3)
            pyxel.text(35, 60, 'Press <space> to start', 7)

            if self.state['count']:
                wpm = (
                    constants.WORD_COUNT /
                    (self.state['end_time'] - self.state['start_time']) * 60
                )
                pyxel.text(45, 80, f'Last WPM: {wpm:.2f}', 7)

        elif self.state['current_scene'] == constants.SCENE_GAME:
            current_word = self.state['current_word'].upper()
            pyxel.text(10, 10, current_word, 7)
            pyxel.text(10, 10, current_word[:self.state['position']], 5)


if __name__ == '__main__':
    Game().run()
