from pyxel_extensions import action


@action
def load_puzzle(state, puzzle):
    return {**state, 'puzzle': puzzle}


def clear_puzzle():
    return load_puzzle(None)
