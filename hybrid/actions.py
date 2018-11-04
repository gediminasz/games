from pyxel_extensions import action


@action
def load_puzzle(state, puzzle):
    assert len(puzzle['top']) == len(puzzle['bottom']) == len(puzzle['goal'])
    return {**state, 'puzzle': puzzle}


def clear_puzzle():
    return load_puzzle(None)


@action
def shift_left(state):
    sequence = state['puzzle']['bottom']
    return {
        **state,
        'puzzle': {
            **state['puzzle'],
            'bottom': sequence[1:] + sequence[0]
        }
    }


@action
def shift_right(state):
    sequence = state['puzzle']['bottom']
    return {
        **state,
        'puzzle': {
            **state['puzzle'],
            'bottom': sequence[-1] + sequence[:-1]
        }
    }
