import sys
sys.path.append('..')

import pygame
import pyxel

import pyxel_extensions.game

import actions
import constants
import reducer
import tabs
import scenes.gameplay


AUDIO_FILE = sys.argv[1]


class Onset(pyxel_extensions.game.Game):
    def __init__(self):
        super().__init__(
            reducer.initial_state(),
            reducer.reducer,
            hot_modules=(
                scenes.gameplay,
            )
        )

        pyxel.image(0).load(0, 0, 'assets/frets.png')

        pygame.init()
        pygame.joystick.init()

        pygame.mixer.init()
        pygame.mixer.music.load(AUDIO_FILE)

        self.store.dispatch(actions.LOAD_TAB, notes=tabs.load_notes(AUDIO_FILE))
        self.store.dispatch(actions.LAUNCH)

    def init_pyxel(self):
        pyxel.init(160, 120, fps=60)

    @property
    def scenes_map(self):
        return {
            constants.SCENE_GAMEPLAY: scenes.gameplay.GameplayScene,
        }

    def update(self):
        pygame.event.pump()
        super().update()

if __name__ == '__main__':
    Onset().run()
