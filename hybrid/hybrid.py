from pyxel_extensions.game import Game

import reducer
import scenes.start


if __name__ == '__main__':
    Game(
        reducer.initial_state(),
        reducer.reducer,
        scenes=(
            scenes.start.StartScene,
        ),
        hot_modules=(
            scenes.start,
        )
    ).run()
