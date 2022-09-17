from copy import deepcopy
from abc import ABCMeta


# порождающий паттерн Прототип
class PrototypeMixin(metaclass=ABCMeta):
    def clone(self):
        return deepcopy(self)
