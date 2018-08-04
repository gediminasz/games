import actions
import constants


def initial_state():
    return {
        'current_scene': None,

        'start_time': None,
        'end_time': None,

        'current_word': None,
        'position': None,
        'words_typed': None,
        'characters_typed': None,

        'points': None,
        'multiplier': None,

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
            'words_typed': (),
            'characters_typed': 0,
            'points': 0,
            'multiplier': 1,
        }

    if action_type == actions.END_GAME:
        return {
            **state,
            'current_scene': constants.SCENE_START,
            'end_time': kwargs['time'],
            'wpm': constants.WORD_COUNT / (kwargs['time'] - state['start_time']) * 60,
            'accuracy': sum(map(len, state['words_typed'])) / state['characters_typed']
        }

    if action_type == actions.TYPE_CHARACTER:
        return {**state, 'characters_typed': state['characters_typed'] + 1}

    if action_type == actions.HIT_CHARACTER:
        return {
            **state,
            'position': state['position'] + 1,
            'points': state['points'] + 1 * state['multiplier']
        }

    if action_type == actions.MISS_CHARACTER:
        return {**state, 'multiplier': 1}

    if action_type == actions.COMPLETE_WORD:
        return {
            **state,
            'words_typed': state['words_typed'] + (state['current_word'],),
            'multiplier': state['multiplier'] + 1,
        }

    if action_type == actions.NEXT_WORD:
        return {
            **state,
            'current_word': kwargs['word'],
            'position': 0,
        }

    return state
