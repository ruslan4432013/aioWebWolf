from time import time

from aioWebWolf.core.services.metaclasses import SingletonByName
from aioWebWolf.core.services.writer import FileWriter


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


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
