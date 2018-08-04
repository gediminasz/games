import time
import pyxel

import actions
import constants


class StartScene:
    def update(self, state, dispatch):
        if pyxel.btnp(pyxel.KEY_SPACE):
            dispatch(actions.START_GAME, time=time.time())
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self, state):
        pyxel.text(70, 40, 'TYPO', 3)
        pyxel.text(35, 60, 'Press <space> to start', 7)
        pyxel.text(55, 70, '<Q> to quit', 7)

        if state['wpm']:
            pyxel.text(45, 80, f"Last WPM: {state['wpm']:.2f}", 7)
