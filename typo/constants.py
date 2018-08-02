SCENE_START = 'SCENE_START'
SCENE_GAME = 'SCENE_GAME'

WORD_COUNT = 5

def load_words(source):
    with open(source, 'r') as f:
        return f.read().split()

ALL_WORDS = load_words('words.txt')
