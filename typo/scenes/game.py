import time

import pyxel

from words import next_word
import actions
import constants


class GameScene:
    def update(self, state, dispatch):
        word_complete = state['position'] == len(state['current_word'])
        if word_complete:
            if state['count'] == constants.WORD_COUNT:
                dispatch(actions.END_GAME, time=time.time())
            else:
                dispatch(actions.NEXT_WORD, word=next_word())

        else:
            current_character = state['current_word'][state['position']]
            if self.input_character == current_character:
                dispatch(actions.TYPE_CHARACTER)

    @property
    def input_character(self):
        for character, key in self.character_map.items():
            if pyxel.btnp(key):
                return character

    def draw(self, state):
        current_word = state['current_word'].upper()
        pyxel.text(10, 10, current_word, 7)
        pyxel.text(10, 10, current_word[:state['position']], 5)

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
