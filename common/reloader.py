import importlib


class Reloader:
    def __init__(self, hot_modules):
        self.hot_modules = hot_modules

    def reload(self):
        print('Reloading...')
        for module in self.hot_modules:
            importlib.reload(module)
