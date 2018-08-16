import sys
sys.path.append('..')

from time import time

from playsound import playsound
import pyxel

from common.store import Store

import actions
import reducer
import tabs


AUDIO_FILE = sys.argv[1]
FRETS_POSITION = 40, 100
FRET_SIZE = 16, 8


class Game:
    def __init__(self):
        pyxel.init(160, 120, fps=60)

        pyxel.image(0).load(0, 0, 'assets/frets.png')

        self.store = Store(reducer.initial_state(), reducer.reducer)

        self.tabs = tabs.load_tabs(AUDIO_FILE)

        self.next_tab = 0
        self.fret = None
        self.fret_hit = False
        self.active_frets = (False,) * 5

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.store.state['playing']:
            self.store.dispatch(actions.START_GAME, time=time())
            # playsound(AUDIO_FILE, block=False)

        else:
            if self.time > self.tabs[self.next_tab]['time']:
                self.fret = tabs.fret(self.tabs[self.next_tab]['strength'])
                self.fret_hit = False
                self.next_tab = min(self.next_tab + 1, len(self.tabs) - 1)

        self.active_frets = [
            0 if pyxel.btn(key) else 1
            for key in (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5)
        ]

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.tabs[self.next_tab]['time'] - self.time < 0.1:
                print('HIT')
                if self.active_frets[self.fret] == 0:  # pressed
                    self.active_frets[self.fret] = 2  # hit
                    self.fret_hit = True
            else:
                print('MISS')

    def draw(self):
        pyxel.cls(0)

        for i, _ in enumerate(tabs.FRETS):
            self.draw_fret(i, 1)

        for i, state in enumerate(self.active_frets):
            self.draw_fret(i, state)

        self.draw_incoming_tabs()

    def draw_fret(self, i, state):
        _, y = FRETS_POSITION
        self.draw_tab(i, y, state)

    def draw_incoming_tabs(self):
        incoming_tabs = [
            tab for tab in self.tabs[self.next_tab:]
            if tab['time'] < self.time + 2  # 2 seconds ahead
        ]

        _, y = FRETS_POSITION
        for tab in incoming_tabs:
            i = tabs.fret(tab['strength'])
            self.draw_tab(i, y - int((tab['time'] - self.time) * 60), 3)

    def draw_tab(self, i, y, state):
        x, _ = FRETS_POSITION
        width, height = FRET_SIZE
        pyxel.blt(x + i * width, y, 0, i * width, state * height, width, height, 0)

    @property
    def time(self):
        return time() - self.store.state['start_time']


if __name__ == '__main__':
    Game().run()
