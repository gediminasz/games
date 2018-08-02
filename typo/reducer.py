from copy import copy
from types import SimpleNamespace

TYPE_CHARACTER = 'TYPE_CHARACTER'
SET_WORD = 'SET_WORD'

def initial_state():
    return {
        'all_words': load_words('words.txt'),
        'current_word': '',
        'position': 0
    }

def load_words(source):
    with open(source, 'r') as f:
        return f.read().split()

def typo_reducer(state, action_type, **kwargs):
    if action_type == TYPE_CHARACTER:
        return {**state, 'position': state['position'] + 1}
    elif action_type == SET_WORD:
        return {**state, 'current_word': kwargs['word'], 'position': 0}
