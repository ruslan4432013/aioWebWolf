from abc import ABC, abstractmethod
import asyncio
from typing import List


class Observer(ABC):

    @abstractmethod
    async def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers: List[Observer] = []

    async def notify(self):
        tasks = [asyncio.create_task(item.update(self)) for item in self.observers]
        await asyncio.wait(tasks)
