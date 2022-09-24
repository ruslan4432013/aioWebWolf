from abc import ABCMeta
from aioWebWolf.core.services import PrototypeMixin, Subject


class User(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name


class Category:
    auto_id = 0

    def __init__(self, name: str, category=None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category: Category = category
        self.courses: list[Course] = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
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
