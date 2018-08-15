import sys
from time import time

from playsound import playsound
import pyxel

from tabs import load_tabs, fret, FRETS


AUDIO_FILE = sys.argv[1]


class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.tabs = load_tabs(AUDIO_FILE)

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
                self.fret = fret(self.tabs[self.next_tab]['strength'])
                self.next_tab = min(self.next_tab + 1, len(self.tabs) - 1)

    def draw(self):
        pyxel.cls(0)


        for i, _ in enumerate(FRETS):
            self.draw_fret(i, pyxel.rectb)

        if self.fret is not None:
            self.draw_fret(self.fret, pyxel.rect)

    def draw_fret(self, i, draw_function):
        width, height = 16, 12
        x, y = 40, 100
        padding = 1
        base_color = 8

        x = x + i * (width + padding)
        draw_function(
            x,
            y,
            x + width,
            y + height,
            base_color + i
        )

    @property
    def time(self):
        return time() - self.start_time

if __name__ == '__main__':
    Game().run()
