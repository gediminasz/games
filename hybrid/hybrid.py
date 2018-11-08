from pyxel_extensions.game import Game

import scenes.gameplay
import scenes.score
import scenes.start


class Hybrid(Game):
    def get_scenes(self):
        return (
            scenes.gameplay.GameplayScene,
            scenes.score.ScoreScene,
            scenes.start.StartScene,
        )


if __name__ == '__main__':
    Hybrid(
        initial_state={
            'puzzle': None,
        },

        initial_scene=scenes.start.StartScene,

        hot_modules=(
            scenes.gameplay,
            scenes.score,
            scenes.start,
        )
    ).run()
