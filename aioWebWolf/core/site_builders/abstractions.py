from abc import ABCMeta

from aioWebWolf.core.orm.unit_of_work import DomainObject
from aioWebWolf.core.services import PrototypeMixin, Subject


class User(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')

        self.courses = []


class Category(DomainObject):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs.get('name')

        if 'id' in kwargs:
            self.id = kwargs.get('id')

        self.courses = []

    def course_count(self):
        result = len(self.courses)
        return result


class Course(PrototypeMixin, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    async def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        await self.notify()
