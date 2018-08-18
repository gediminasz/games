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

    def update(self):
        if not self.store.state['playing']:
            self.store.dispatch(actions.START_GAME, time=time())
            pygame.mixer.music.play()

        self.activate_frets()
        self.strum()

    def activate_frets(self):
        keyboard_frets = map(pyxel.btn, (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5))
        joystick_frets = map(self.joystick.get_button, (1, 2, 3, 0, 4))
        frets = tuple(
            bool(keyboard | joystick)
            for keyboard, joystick in zip(keyboard_frets, joystick_frets)
        )

        if frets != self.store.state['frets']:
            self.store.dispatch(actions.ACTIVATE_FRETS, frets=frets)

    def strum(self):
        is_strumming = pyxel.btn(pyxel.KEY_SPACE) or self.joystick.get_hat(0)[1]
        strum = not self.store.state['strum'] and is_strumming

        if is_strumming != self.store.state['strum']:
            self.store.dispatch(actions.SET_STRUM, strum=strum)

        note = next(self.upcoming_notes, None)
        if strum:
            if note and not note['hit'] and self.note_hit(note):
                self.store.dispatch(actions.NOTE_HIT, note=note)
            else:
                self.store.dispatch(actions.NOTE_MISS)

    def note_hit(self, note):
        if not note:
            return False

        fret = tabs.fret(note['strength'])
        chord = tuple(i == fret for i in range(len(constants.FRETS)))

        return (
            tabs.within_time_window(note, self.time) and
            self.store.state['frets'] == chord
        )

    def draw(self):
        for fret, active in enumerate(self.store.state['frets']):
            self.draw_fret(
                fret,
                constants.ASSETS_FRET_ACTIVE if active else constants.ASSETS_FRET_INACTIVE
            )

        self.draw_upcoming_notes()

        pyxel.text(2, 2, f"Streak: {self.store.state['streak']}", 7)

    def draw_upcoming_notes(self):
        _, y = constants.FRETS_POSITION
        for note in self.upcoming_notes:
            i = tabs.fret(note['strength'])
            self.draw_note(i, y - int((note['time'] - self.time) * constants.SPEED), constants.ASSETS_NOTE)

    def draw_note(self, i, y, asset):
        x, _ = constants.FRETS_POSITION
        width, height = constants.FRET_SIZE
        pyxel.blt(x + i * width, y, 0, i * width, asset * height, width, height, 0)

    def draw_fret(self, i, asset):
        _, y = constants.FRETS_POSITION
        self.draw_note(i, y, asset)

    @property
    def upcoming_notes(self):  # TODO stop calling this so often, optimize
        current_time = self.time
        return (
            note for note in self.store.state['notes']
            if (current_time < note['time'] < (current_time + constants.DRAW_SECONDS_AHEAD))
            and not note['hit']
        )

    @property
    def time(self):
        return time() - self.store.state['start_time']
