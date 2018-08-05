from reducer import initial_state, reducer

class Store:
    def __init__(self):
        self.state = initial_state()
        self.subscribers = []

    def dispatch(self, action_type, **kwargs):
        print(action_type, kwargs)

        new_state = reducer(self.state, action_type, **kwargs)

        for subscriber in self.subscribers:
            subscriber(self.state, new_state)

        self.state = new_state
        return new_state

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
