from collections import defaultdict

import actions
import constants


def initial_state():
    return {
        'current_scene': None,
        'start_time': None,
        'end_time': None,
        'current_word': None,
        'position': None,
        'count': None,
    }

def typo_reducer(state, action_type, **kwargs):
    if action_type == actions.LAUNCH:
        return {**state, 'current_scene': constants.SCENE_START}

    elif action_type == actions.START_GAME:
        return {
            **state,
            'current_scene': constants.SCENE_GAME,
            'start_time': kwargs['time'],
            'current_word': '',
            'position': 0,
            'count': 0,
        }

    elif action_type == actions.END_GAME:
        return {
            **state,
            'current_scene': constants.SCENE_START,
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
