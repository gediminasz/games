import pyxel

from reducer import initial_state, reducer
from scenes.game import GameScene
from scenes.start import StartScene
import actions
import constants


SCENES_MAP = {
    constants.SCENE_START: StartScene,
    constants.SCENE_GAME: GameScene,
}


class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.state = initial_state()
        self.scene = None

        self.dispatch(actions.LAUNCH)

    def dispatch(self, action_type, **kwargs):
        print(action_type, kwargs)

        new_state = reducer(self.state, action_type, **kwargs)
        self.change_scene(new_state['current_scene'])
        self.state = new_state
        return new_state

    def change_scene(self, scene_name):
        if scene_name != self.state['current_scene']:
            self.scene = SCENES_MAP[scene_name]()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        self.scene.update(self.state, self.dispatch)

    def draw(self):
        pyxel.cls(0)
        self.scene.draw(self.state)


if __name__ == '__main__':
    Game().run()
