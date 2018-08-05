import importlib

import pyxel

from reducer import initial_state, reducer
import actions
import constants
import scenes.start
import scenes.game


HOT_MODULES = (
    scenes.start,
    scenes.game
)


class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.state = initial_state()
        self.scene = None

        self.dispatch(actions.LAUNCH)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_F1):
            print('Reloading...')
            for module in HOT_MODULES:
                importlib.reload(module)
            self.scene = self.build_scene(self.state['current_scene'])

        self.scene.update(self.state, self.dispatch)

    def draw(self):
        pyxel.cls(0)
        self.scene.draw(self.state)

    def dispatch(self, action_type, **kwargs):
        print(action_type, kwargs)

        new_state = reducer(self.state, action_type, **kwargs)
        self.change_scene(new_state['current_scene'])
        self.state = new_state
        return new_state

    def change_scene(self, scene_name):
        if scene_name != self.state['current_scene']:
            self.scene = self.build_scene(scene_name)

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
