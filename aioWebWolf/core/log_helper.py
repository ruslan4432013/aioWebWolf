from time import time

from .metaclasses import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print(f'log---> {text}')


class Debugger:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            async def timed(*args, **kwargs):
                start = time()
                result = await method(*args, **kwargs)
                delta = time() - start

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
