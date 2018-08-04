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

        'characters_typed': None,
        'characters_hit': None,

        'wpm': None,
        'accuracy': None,
    }


def reducer(state, action_type, **kwargs):
    if action_type == actions.LAUNCH:
        return {**state, 'current_scene': constants.SCENE_START}

    if action_type == actions.START_GAME:
        return {
            **state,
            'current_scene': constants.SCENE_GAME,
            'start_time': kwargs['time'],
            'current_word': kwargs['word'],
            'position': 0,
            'count': 0,
            'characters_typed': 0,
            'characters_hit': 0,
        }

    if action_type == actions.END_GAME:
        return {
            **state,
            'current_scene': constants.SCENE_START,
            'end_time': kwargs['time'],
            'wpm': (
                constants.WORD_COUNT /
                (kwargs['time'] - state['start_time']) * 60
            ),
            'accuracy': state['characters_hit'] / state['characters_typed']
        }

    if action_type == actions.TYPE_CHARACTER:
        return {**state, 'characters_typed': state['characters_typed'] + 1}

    if action_type == actions.HIT_CHARACTER:
        return {
            **state,
            'position': state['position'] + 1,
            'characters_hit': state['characters_hit'] + 1,
        }

    if action_type == actions.NEXT_WORD:
        return {
            **state,
            'current_word': kwargs['word'],
            'position': 0,
            'count': state['count'] + 1
        }

    return state
