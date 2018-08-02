from types import SimpleNamespace
import pyxel

class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.state = SimpleNamespace(
            remaining_input='typo',
            words_typed=1
        )

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state.remaining_input:
            for character, key in self.character_map.items():
                if self.state.remaining_input[0] == character and pyxel.btnp(key):
                    self.state.remaining_input = self.state.remaining_input[1:]
                    break

        else:
            self.state.words_typed += 1
            self.state.remaining_input = 'typo'

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, str(self.state.remaining_input), 7)

    @property
    def character_map(self):
        return {
            'o': pyxel.KEY_O,
            'p': pyxel.KEY_P,
            't': pyxel.KEY_T,
            'y': pyxel.KEY_Y,
        }


if __name__ == '__main__':
    Game().run()
