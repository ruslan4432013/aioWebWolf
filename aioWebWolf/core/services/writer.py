from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write(self, text):
        pass


class ConsoleWriter(Writer):
    def write(self, text):
        print(text)


class FileWriter(Writer):

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
