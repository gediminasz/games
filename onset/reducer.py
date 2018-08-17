import actions
import constants


def initial_state():
    return {
        '__scene__': None,

        'tab': None,
        'playing': False,
        'start_time': None,
        'frets': constants.INITIAL_ACTIVE_FRETS,
        'strum': False,
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
        }

    if action_type == actions.LOAD_TAB:
        return {**state, 'tab': kwargs['tab']}

    if action_type == actions.ACTIVATE_FRETS:
        return {**state, 'frets': kwargs['frets']}

    if action_type == actions.SET_STRUM:
        return {**state, 'strum': kwargs['strum']}

    return state
