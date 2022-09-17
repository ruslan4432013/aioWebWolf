from .metaclasses import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print(f'log---> {text}')
