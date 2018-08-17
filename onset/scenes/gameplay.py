from operator import or_
from time import time

import pygame
import pyxel

from common.scene import Scene

import actions
import constants
import tabs


class GameplayScene(Scene):
    def __init__(self, scene):
        super().__init__(scene)

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.previous_strum = self.joystick.get_hat(0)[1]

    def update(self):
        if not self.store.state['playing']:
            self.store.dispatch(actions.START_GAME, time=time())
            pygame.mixer.music.play()

        self.activate_frets()
        self.strum()

    def activate_frets(self):
        keyboard_frets = map(pyxel.btn, (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5))
        joystick_frets = map(self.joystick.get_button, (1, 2, 3, 0, 4))
        frets = [
            keyboard | joystick
            for keyboard, joystick in zip(keyboard_frets, joystick_frets)
        ]

        if frets != self.store.state['active_frets']:
            self.store.dispatch(actions.ACTIVATE_FRETS, frets=frets)

    def strum(self):
        current_strum = self.joystick.get_hat(0)[1]
        did_strum = not self.previous_strum and current_strum
        self.previous_strum = current_strum

        if pyxel.btnp(pyxel.KEY_SPACE) or did_strum:
            if self.note_hit():
                print('HIT')
            else:
                print('MISS')

    def draw(self):
        for fret, active in enumerate(self.store.state['active_frets']):
            self.draw_fret(
                fret,
                constants.ASSETS_FRET_ACTIVE if active else constants.ASSETS_FRET_INACTIVE
            )

        self.draw_upcoming_notes()

    def draw_upcoming_notes(self):
        _, y = constants.FRETS_POSITION
        for note in self.upcoming_notes():
            i = tabs.fret(note['strength'])
            self.draw_note(i, y - int((note['time'] - self.time()) * constants.SPEED), constants.ASSETS_NOTE)

    def draw_note(self, i, y, asset):
        x, _ = constants.FRETS_POSITION
        width, height = constants.FRET_SIZE
        pyxel.blt(x + i * width, y, 0, i * width, asset * height, width, height, 0)

    def draw_fret(self, i, asset):
        _, y = constants.FRETS_POSITION
        self.draw_note(i, y, asset)

    def note_hit(self):
        next_note = next(self.upcoming_notes(), None)
        if not next_note:
            return False

        fret = tabs.fret(next_note['strength'])
        return (
            ((next_note['time'] - self.time()) < constants.NOTE_WINDOW) and
            self.store.state['active_frets'][fret]
        )

    def upcoming_notes(self):  # TODO stop calling this so often, optimize
        current_time = self.time()
        return (
            note for note in self.store.state['tab']
            if current_time < note['time'] < (current_time + constants.DRAW_SECONDS_AHEAD)
        )

    def time(self):
        return time() - self.store.state['start_time']
