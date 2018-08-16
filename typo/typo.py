import sys
sys.path.append('..')

import pyxel

from common.reloader import Reloader
from common.store import Store

import actions
import constants
import reducer
import scenes.game
import scenes.start


class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.store = Store(reducer.initial_state(), reducer.reducer)
        self.store.subscribe(self.change_scene)

        self.reloader = Reloader((
            scenes.start,
            scenes.game
        ))

        self.scene = None

        self.store.dispatch(actions.LAUNCH)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_F1):
            self.reloader.reload()
            self.scene = self.build_scene(self.store.state['current_scene'])

        self.scene.update(self.store.state, self.store.dispatch)

    def draw(self):
        pyxel.cls(0)
        self.scene.draw(self.store.state)

    def change_scene(self, old_state, new_state):
        if new_state['current_scene'] != old_state['current_scene']:
            self.scene = self.build_scene(new_state['current_scene'])

    def build_scene(self, name):
        return self.scenes_map[name]()

    @property
    def scenes_map(self):
        return {
            constants.SCENE_START: scenes.start.StartScene,
            constants.SCENE_GAME: scenes.game.GameScene,
        }


if __name__ == '__main__':
    Game().run()
