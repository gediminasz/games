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

DRAW_SECONDS_AHEAD = 2
SPEED = 60
NOTE_WINDOW = 0.1  # second

ASSETS_FRET_INACTIVE = 0
ASSETS_FRET_ACTIVE = 1
ASSETS_FRET_HIT = 2
ASSETS_NOTE = 3
ASSETS_NOTE_SMALL = 4


class Game:
    def __init__(self):
        pyxel.init(160, 120, fps=60)

        pyxel.image(0).load(0, 0, 'assets/frets.png')

        self.store = Store(reducer.initial_state(), reducer.reducer)

        self.tabs = tabs.load_tabs(AUDIO_FILE)

        self.next_tab = 0
        self.fret = None

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.store.state['playing']:
            self.store.dispatch(actions.START_GAME, time=time())
            # playsound(AUDIO_FILE, block=False)

        else:
            if self.time > self.tabs[self.next_tab]['time']:
                self.fret = tabs.fret(self.tabs[self.next_tab]['strength'])
                self.next_tab = min(self.next_tab + 1, len(self.tabs) - 1)

        if any(map(pyxel.btnp, self.fret_keys)) or any(map(pyxel.btnr, self.fret_keys)):
            self.store.dispatch(
                actions.ACTIVATE_FRETS,
                frets=[pyxel.btn(key) for key in self.fret_keys]
            )

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.note_hit:
                print('HIT')
            else:
                print('MISS')

    def draw(self):
        pyxel.cls(0)

        for fret, active in enumerate(self.store.state['active_frets']):
            self.draw_fret(fret, ASSETS_FRET_ACTIVE if active else ASSETS_FRET_INACTIVE)

        self.draw_incoming_tabs()

    def draw_fret(self, i, state):
        _, y = FRETS_POSITION
        self.draw_tab(i, y, state)

    def draw_incoming_tabs(self):
        incoming_tabs = [
            tab for tab in self.tabs[self.next_tab:]
            if tab['time'] < self.time + DRAW_SECONDS_AHEAD
        ]

        _, y = FRETS_POSITION
        for tab in incoming_tabs:
            i = tabs.fret(tab['strength'])
            self.draw_tab(i, y - int((tab['time'] - self.time) * SPEED), ASSETS_NOTE)

    def draw_tab(self, i, y, state):
        x, _ = FRETS_POSITION
        width, height = FRET_SIZE
        pyxel.blt(x + i * width, y, 0, i * width, state * height, width, height, 0)

    @property
    def time(self):
        return time() - self.store.state['start_time']

    @property
    def fret_keys(self):
        return (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5)

    @property
    def note_hit(self):
        return (
            (self.tabs[self.next_tab]['time'] - self.time < NOTE_WINDOW) and
            self.store.state['active_frets'][self.fret]
        )


if __name__ == '__main__':
    Game().run()
