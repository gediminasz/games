from pyxel_extensions import action


@action
def load_puzzle(state, puzzle):
    assert (puzzle is None) or (len(puzzle['top']) == len(puzzle['bottom']) == len(puzzle['goal']))
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


@action
def crossover(state):
    crossover = state['puzzle']['crossover']
    top = state['puzzle']['top']
    bottom = state['puzzle']['bottom']

    return {
        **state,
        'puzzle': {
            **state['puzzle'],
            'top': top[:crossover] + bottom[crossover:],
            'bottom': bottom[:crossover] + top[crossover:],
        }
    }


@action
def flip(state):
    return {
        **state,
        'puzzle': {
            **state['puzzle'],
            'top': state['puzzle']['bottom'],
            'bottom': state['puzzle']['top']
        }
    }
