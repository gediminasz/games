import time
import pyxel

from common.scene import Scene

from words import next_word
import actions


class StartScene(Scene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.store.dispatch(actions.START_GAME, time=time.time(), word=next_word())
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.text(70, 40, 'TYPO', 3)
        pyxel.text(35, 60, 'Press <space> to start', 7)
        pyxel.text(55, 70, '<Q> to quit', 7)

        if self.store.state['wpm']:
            pyxel.text(45, 90, f"Last WPM: {self.store.state['wpm']:.2f}", 7)
        if self.store.state['accuracy']:
            pyxel.text(45, 100, f"Accuracy: {self.store.state['accuracy'] * 100:.2f}%", 7)
        if self.store.state['points']:
            pyxel.text(45, 110, f"Points: {self.store.state['points']}", 7)
