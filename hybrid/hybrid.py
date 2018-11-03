from pyxel_extensions.game import Game

import scenes.start
import scenes.gameplay


if __name__ == '__main__':
    Game(
        initial_state={},
        scenes=(
            scenes.start.StartScene,
            scenes.gameplay.GameplayScene,
        ),
        initial_scene=scenes.start.StartScene,
        hot_modules=(
            scenes.start,
            scenes.gameplay,
        )
    ).run()
