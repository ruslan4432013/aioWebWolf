from abc import ABCMeta
from .mixins import PrototypeMixin


class User(metaclass=ABCMeta):
    pass


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


class Course(PrototypeMixin):

    def __init__(self, name: str, category: Category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
