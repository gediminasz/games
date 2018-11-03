import actions
import constants


def initial_state():
    return {
        '__scene__': None,
    }


def reducer(state, action_type, **kwargs):
    if action_type == actions.LAUNCH:
        return {**state, '__scene__': constants.SCENE_START}

    return state
