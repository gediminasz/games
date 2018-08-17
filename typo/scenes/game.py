import time

import pyxel

from common.scene import Scene

from words import next_word
import actions
import constants


class GameScene(Scene):
    def update(self):
        word_complete = self.store.state['position'] == len(self.store.state['current_word'])
        if word_complete:
            state = self.store.dispatch(actions.COMPLETE_WORD)

            if len(self.store.state['words_typed']) == constants.WORD_COUNT:
                self.store.dispatch(actions.END_GAME, time=time.time())
            else:
                self.store.dispatch(actions.NEXT_WORD, word=next_word())

        else:
            current_character = self.store.state['current_word'][self.store.state['position']]
            if self.input_character:
                self.store.dispatch(actions.TYPE_CHARACTER)
                if self.input_character == current_character:
                    self.store.dispatch(actions.HIT_CHARACTER)
                else:
                    self.store.dispatch(actions.MISS_CHARACTER)

    @property
    def input_character(self):
        for character, key in self.character_map.items():
            if pyxel.btnp(key):
                return character

    def draw(self):
        current_word = self.store.state['current_word'].upper()
        pyxel.text(10, 60, current_word, 7)
        pyxel.text(10, 60, current_word[:self.store.state['position']], 5)
        pyxel.text(10, 10, f"{self.store.state['points']} (x{self.store.state['multiplier']})", 8)

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
