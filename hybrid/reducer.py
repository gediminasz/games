from scenes.start import StartScene


def initial_state():
    return {
        '__scene__': StartScene.name,
    }


def reducer(state, action_type, **kwargs):
    return state
