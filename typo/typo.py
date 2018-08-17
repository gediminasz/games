import sys
sys.path.append('..')

import common.game

import actions
import constants
import reducer
import scenes.game
import scenes.start


class Typo(common.game.Game):
    def __init__(self):
        super().__init__(
            reducer.initial_state(),
            reducer.reducer,
            hot_modules=(
                scenes.game,
                scenes.start,
            )
        )

        self.store.dispatch(actions.LAUNCH)

    @property
    def scenes_map(self):
        return {
            constants.SCENE_START: scenes.start.StartScene,
            constants.SCENE_GAME: scenes.game.GameScene,
        }


if __name__ == '__main__':
    Typo().run()
