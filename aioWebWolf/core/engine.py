from .models import Teacher, Student, Course
from .abstractions import Category
from .factory import UserFactory, CourseFactory
from .metaclasses import Singleton


class Engine(metaclass=Singleton):
    def __init__(self):
        self.teachers: list[Teacher] = []
        self.students: list[Student] = []
        self.courses: list[Course] = []
        self.categories: list[Category] = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category: Category = None):
        return Category(name, category)

    def find_category_by_id(self, category_id: int):
        for item in self.categories:
            print('item', item.id)
            if item.id == category_id:
                return item
        raise Exception(f'Нет категории с id = {category_id}')

    @staticmethod
    def create_course(type_: str, name: str, category: Category) -> Course:
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None
