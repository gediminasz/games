import actions
import constants


def initial_state():
    return {
        '__scene__': None,

        'notes': None,
        'playing': False,
        'start_time': None,
        'frets': constants.INITIAL_ACTIVE_FRETS,
        'strum': False,
        'streak': 0,
    }


def reducer(state, action_type, **kwargs):
    if action_type == actions.LAUNCH:
        return {**state, '__scene__': constants.SCENE_GAMEPLAY}

    if action_type == actions.START_GAME:
        return {
            **state,
            'playing': True,
            'start_time': kwargs['time'],
            'frets': constants.INITIAL_ACTIVE_FRETS,
            'strum': False,
            'streak': 0,
        }

    if action_type == actions.LOAD_TAB:
        return {**state, 'notes': kwargs['notes']}

    if action_type == actions.ACTIVATE_FRETS:
        return {**state, 'frets': kwargs['frets']}

    if action_type == actions.SET_STRUM:
        return {**state, 'strum': kwargs['strum']}

    if action_type == actions.NOTE_HIT:
        index = kwargs['note']['index']
        notes = [
            {**note, 'hit': True if note['index'] == index else note['hit']}
            for note in state['notes']
        ]
        return {**state, 'notes': notes, 'streak': state['streak'] + 1}

    if action_type == actions.NOTE_MISS:
        return {**state, 'streak': 0}

    return state
