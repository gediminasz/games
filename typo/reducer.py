from copy import copy
from types import SimpleNamespace

TYPE_CHARACTER = 'TYPE_CHARACTER'
SET_WORD = 'SET_WORD'

def initial_state():
    return {
        'all_words': load_words('words.txt'),
        'remaining_input': '',
        'words_typed': 0
    }

def load_words(source):
    with open(source, 'r') as f:
        return f.read().split()

def typo_reducer(state, action_type, **kwargs):
    if action_type == TYPE_CHARACTER:
        return {**state, 'remaining_input': state['remaining_input'][1:]}
    elif action_type == SET_WORD:
        return {**state, 'remaining_input': kwargs['word']}
