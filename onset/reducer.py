import actions

INITIAL_ACTIVE_FRETS = (False,) * 5

def initial_state():
    return {
        'playing': False,
        'start_time': None,
        'active_frets': INITIAL_ACTIVE_FRETS,
    }


def reducer(state, action_type, **kwargs):
    if action_type == actions.START_GAME:
        return {
            **state,
            'playing': True,
            'start_time': kwargs['time'],
            'active_frets': INITIAL_ACTIVE_FRETS,
        }

    if action_type == actions.ACTIVATE_FRETS:
        return {**state, 'active_frets': kwargs['frets']}

    return state
