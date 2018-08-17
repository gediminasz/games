from time import time

import pygame
import pyxel

import actions
import constants
import tabs


class GameplayScene:
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.previous_strum = self.joystick.get_hat(0)[1]

    def update(self, state, dispatch):
        if not state['playing']:
            dispatch(actions.START_GAME, time=time())
            pygame.mixer.music.play()

        if any(map(pyxel.btnp, self.fret_keys)) or any(map(pyxel.btnr, self.fret_keys)):
            dispatch(
                actions.ACTIVATE_FRETS,
                frets=[pyxel.btn(key) for key in self.fret_keys]
            )

        pygame.event.pump()

        joystick_frets = [self.joystick.get_button(button) for button in [1, 2, 3, 0, 4]]
        if joystick_frets != state['active_frets']:
            dispatch(actions.ACTIVATE_FRETS, frets=joystick_frets)

        current_strum = self.joystick.get_hat(0)[1]
        did_strum = not self.previous_strum and current_strum
        self.previous_strum = current_strum

        if pyxel.btnp(pyxel.KEY_SPACE) or did_strum:
            if self.note_hit(state):
                print('HIT')
            else:
                print('MISS')

    def draw(self, state):
        for fret, active in enumerate(state['active_frets']):
            self.draw_fret(
                fret,
                constants.ASSETS_FRET_ACTIVE if active else constants.ASSETS_FRET_INACTIVE
            )

        self.draw_upcoming_notes(state)

    def draw_upcoming_notes(self, state):
        _, y = constants.FRETS_POSITION
        for note in self.upcoming_notes(state):
            i = tabs.fret(note['strength'])
            self.draw_note(i, y - int((note['time'] - self.time(state)) * constants.SPEED), constants.ASSETS_NOTE)

    def draw_note(self, i, y, asset):
        x, _ = constants.FRETS_POSITION
        width, height = constants.FRET_SIZE
        pyxel.blt(x + i * width, y, 0, i * width, asset * height, width, height, 0)

    def draw_fret(self, i, asset):
        _, y = constants.FRETS_POSITION
        self.draw_note(i, y, asset)

    @property
    def fret_keys(self):
        return (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5)

    def note_hit(self, state):
        next_note = next(self.upcoming_notes(state), None)
        if not next_note:
            return False

        fret = tabs.fret(next_note['strength'])
        return (
            ((next_note['time'] - self.time(state)) < constants.NOTE_WINDOW) and
            state['active_frets'][fret]
        )

    def upcoming_notes(self, state):  # TODO stop calling this so often, optimize
        current_time = self.time(state)
        return (
            note for note in state['tab']
            if current_time < note['time'] < (current_time + constants.DRAW_SECONDS_AHEAD)
        )

    def time(self, state):
        return time() - state['start_time']
