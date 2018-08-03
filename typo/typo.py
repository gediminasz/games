import pyxel

from reducer import initial_state, typo_reducer
from scenes.game import GameScene
from scenes.start import StartScene
import constants


class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.state = initial_state()

    def dispatch(self, action_type, **kwargs):
        self.state = typo_reducer(self.state, action_type, **kwargs)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state['current_scene'] == constants.SCENE_START:
            StartScene().update(self.state, self.dispatch)

        if self.state['current_scene'] == constants.SCENE_GAME:
            GameScene().update(self.state, self.dispatch)

    def draw(self):
        pyxel.cls(0)

        if self.state['current_scene'] == constants.SCENE_START:
            StartScene().draw(self.state)

        elif self.state['current_scene'] == constants.SCENE_GAME:
            GameScene().draw(self.state)


if __name__ == '__main__':
    Game().run()
