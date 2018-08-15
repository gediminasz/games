import sys
from time import time

from playsound import playsound
import pyxel

import tabs


AUDIO_FILE = sys.argv[1]
FRETS_POSITION = 40, 100
FRET_SIZE = 16, 8


class Game:
    def __init__(self):
        pyxel.init(160, 120, fps=60)

        pyxel.image(0).load(0, 0, 'assets/frets.png')

        self.tabs = tabs.load_tabs(AUDIO_FILE)

        self.start_time = None
        self.playing = False

        self.next_tab = 0
        self.fret = None

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.playing:
            self.playing = True
            self.start_time = time()
            playsound(AUDIO_FILE, block=False)

        else:
            if self.time > self.tabs[self.next_tab]['time']:
                self.fret = tabs.fret(self.tabs[self.next_tab]['strength'])
                self.next_tab = min(self.next_tab + 1, len(self.tabs) - 1)

    def draw(self):
        pyxel.cls(0)

        for i, _ in enumerate(tabs.FRETS):
            self.draw_fret(i, 1)

        if self.fret is not None:
            self.draw_fret(self.fret, 0)

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
        return time() - self.start_time

if __name__ == '__main__':
    Game().run()
