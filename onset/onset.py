import sys
sys.path.append('..')

from time import time

import pygame
import pyxel

import common.game

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


class Onset(common.game.Game):
    def __init__(self):
        super().__init__(reducer.initial_state(), reducer.reducer)

        pyxel.image(0).load(0, 0, 'assets/frets.png')

        self.tab = tabs.load_tab(AUDIO_FILE)

        self.next_tab = 0

        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.previous_strum = self.joystick.get_hat(0)[1]

        pygame.mixer.init()
        pygame.mixer.music.load(AUDIO_FILE)

    def init_pyxel(self):
        pyxel.init(160, 120, fps=60)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.store.state['playing']:
            self.store.dispatch(actions.START_GAME, time=time())
            pygame.mixer.music.play()

        if any(map(pyxel.btnp, self.fret_keys)) or any(map(pyxel.btnr, self.fret_keys)):
            self.store.dispatch(
                actions.ACTIVATE_FRETS,
                frets=[pyxel.btn(key) for key in self.fret_keys]
            )

        pygame.event.pump()

        joystick_frets = [self.joystick.get_button(button) for button in [1, 2, 3, 0, 4]]
        if joystick_frets != self.store.state['active_frets']:
            self.store.dispatch(actions.ACTIVATE_FRETS, frets=joystick_frets)

        current_strum = self.joystick.get_hat(0)[1]
        did_strum = not self.previous_strum and current_strum
        self.previous_strum = current_strum

        if pyxel.btnp(pyxel.KEY_SPACE) or did_strum:
            if self.note_hit:
                print('HIT')
            else:
                print('MISS')

    def draw(self):
        pyxel.cls(0)

        for fret, active in enumerate(self.store.state['active_frets']):
            self.draw_fret(fret, ASSETS_FRET_ACTIVE if active else ASSETS_FRET_INACTIVE)

        self.draw_upcoming_notes()

    def draw_fret(self, i, asset):
        _, y = FRETS_POSITION
        self.draw_note(i, y, asset)

    def draw_upcoming_notes(self):
        _, y = FRETS_POSITION
        for note in self.upcoming_notes:
            i = tabs.fret(note['strength'])
            self.draw_note(i, y - int((note['time'] - self.time) * SPEED), ASSETS_NOTE)

    def draw_note(self, i, y, asset):
        x, _ = FRETS_POSITION
        width, height = FRET_SIZE
        pyxel.blt(x + i * width, y, 0, i * width, asset * height, width, height, 0)

    @property
    def fret_keys(self):
        return (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5)

    @property
    def note_hit(self):
        next_note = next(self.upcoming_notes, None)
        if not next_note:
            return False

        fret = tabs.fret(next_note['strength'])
        return (
            ((next_note['time'] - self.time) < NOTE_WINDOW) and
            self.store.state['active_frets'][fret]
        )

    @property
    def upcoming_notes(self):  # TODO stop calling this so often, optimize
        return (
            note for note in self.tab
            if self.time < note['time'] < (self.time + DRAW_SECONDS_AHEAD)
        )

    @property
    def time(self):
        return time() - self.store.state['start_time']


if __name__ == '__main__':
    Onset().run()
