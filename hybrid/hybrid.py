import json

import pyxel
from pyxel_extensions.game import Game

import scenes.gameplay
import scenes.score
import scenes.start
from actions import load_puzzles


class Hybrid(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyxel.load('assets/graphics.pyxel')
        self.load_puzzles()

    def get_scenes(self):
        return (
            scenes.gameplay.GameplayScene,
            scenes.score.ScoreScene,
            scenes.start.StartScene,
        )

    def load_puzzles(self):
        with open('puzzles.json', 'r') as source:
            puzzles = json.load(source)['puzzles']
        self.store.dispatch(load_puzzles(puzzles))


if __name__ == '__main__':
    Hybrid(
        initial_state={
            'puzzles': None,
            'puzzle': None,
        },

        initial_scene=scenes.start.StartScene,

        hot_modules=(
            scenes.gameplay,
            scenes.score,
            scenes.start,
        )
    ).run()
