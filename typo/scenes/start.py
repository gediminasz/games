import time
import pyxel

from words import next_word
import actions
import constants


class StartScene:
    def update(self, state, dispatch):
        if pyxel.btnp(pyxel.KEY_SPACE):
            dispatch(actions.START_GAME, time=time.time(), word=next_word())
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self, state):
        pyxel.text(70, 40, 'TYPO', 3)
        pyxel.text(35, 60, 'Press <space> to start', 7)
        pyxel.text(55, 70, '<Q> to quit', 7)

        if state['wpm']:
            pyxel.text(45, 90, f"Last WPM: {state['wpm']:.2f}", 7)
        if state['accuracy']:
            pyxel.text(45, 100, f"Accuracy: {state['accuracy'] * 100:.2f}%", 7)
