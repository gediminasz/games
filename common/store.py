import reprlib


class Store:
    def __init__(self, initial_state, reducer):
        self.state = initial_state
        self.reducer = reducer
        self.subscribers = []

    def dispatch(self, action_type, **kwargs):
        print(action_type, reprlib.repr(kwargs))

        new_state = self.reducer(self.state, action_type, **kwargs)

        for subscriber in self.subscribers:
            subscriber(self.state, new_state)

        self.state = new_state
        return new_state

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
