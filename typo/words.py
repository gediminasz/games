from random import choice

import constants

def load_words(source):
    with open(source, 'r') as f:
        return f.read().split()

def next_word():
    return choice(constants.ALL_WORDS)
