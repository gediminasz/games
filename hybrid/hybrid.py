from pyxel_extensions.game import Game

import scenes.start
import scenes.gameplay


class Hybrid(Game):
    def get_scenes(self):
        return (
            scenes.start.StartScene,
            scenes.gameplay.GameplayScene,
        )


if __name__ == '__main__':
    Hybrid(
        initial_state={
            'puzzle': None,
        },

        initial_scene=scenes.start.StartScene,

        hot_modules=(
            scenes.start,
            scenes.gameplay,
        )
    ).run()
