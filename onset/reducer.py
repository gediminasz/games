import actions


def initial_state():
    return {
        'playing': False,
        'start_time': None,
    }


def reducer(state, action_type, **kwargs):
    if action_type == actions.START_GAME:
        return {
            **state,
            'playing': True,
            'start_time': kwargs['time'],
        }

    return state
