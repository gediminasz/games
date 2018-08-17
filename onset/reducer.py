import actions
import constants


def initial_state():
    return {
        '__scene__': None,

        'tab': None,
        'playing': False,
        'start_time': None,
        'active_frets': constants.INITIAL_ACTIVE_FRETS,
    }


def reducer(state, action_type, **kwargs):
    if action_type == actions.LAUNCH:
        return {**state, '__scene__': constants.SCENE_GAMEPLAY}

    if action_type == actions.START_GAME:
        return {
            **state,
            'playing': True,
            'start_time': kwargs['time'],
            'active_frets': constants.INITIAL_ACTIVE_FRETS,
        }

    if action_type == actions.LOAD_TAB:
        return {**state, 'tab': kwargs['tab']}

    if action_type == actions.ACTIVATE_FRETS:
        return {**state, 'active_frets': kwargs['frets']}

    return state
