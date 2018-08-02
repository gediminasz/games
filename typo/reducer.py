from copy import copy
from types import SimpleNamespace

import actions

SCENE_START = 'SCENE_START'
SCENE_GAME = 'SCENE_GAME'

def initial_state():
    return {
        'current_scene': SCENE_START,
        'all_words': load_words('words.txt'),
        'start_time': None,
        'end_time': None,
        'current_word': '',
        'position': 0,
        'count': 0,
    }

def load_words(source):
    with open(source, 'r') as f:
        return f.read().split()

def typo_reducer(state, action_type, **kwargs):
    if action_type == actions.START_GAME:
        return {
            **state,
            'current_scene': SCENE_GAME,
            'start_time': kwargs['time'],
            'current_word': '',
            'position': 0,
            'count': 0,
        }

    elif action_type == actions.END_GAME:
        return {
            **state,
            'current_scene': SCENE_START,
            'end_time': kwargs['time']
        }

    elif action_type == actions.TYPE_CHARACTER:
        return {**state, 'position': state['position'] + 1}

    elif action_type == actions.NEXT_WORD:
        return {
            **state,
            'current_word': kwargs['word'],
            'position': 0,
            'count': state['count'] + 1
        }
