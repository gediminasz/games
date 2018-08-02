from copy import copy
from types import SimpleNamespace

START_GAME = 'START_GAME'
END_GAME = 'END_GAME'

TYPE_CHARACTER = 'TYPE_CHARACTER'
NEXT_WORD = 'NEXT_WORD'

SCENE_START = 'SCENE_START'
SCENE_GAME = 'SCENE_GAME'

def initial_state():
    return {
        'current_scene': SCENE_START,
        'all_words': load_words('words.txt'),
        'current_word': '',
        'position': 0,
        'count': 0,
    }

def load_words(source):
    with open(source, 'r') as f:
        return f.read().split()

def typo_reducer(state, action_type, **kwargs):
    if action_type == START_GAME:
        return {**initial_state(), 'current_scene': SCENE_GAME}
    elif action_type == END_GAME:
        return {**state, 'current_scene': SCENE_START}

    elif action_type == TYPE_CHARACTER:
        return {**state, 'position': state['position'] + 1}
    elif action_type == NEXT_WORD:
        return {
            **state,
            'current_word': kwargs['word'],
            'position': 0,
            'count': state['count'] + 1
        }
