from . import User, Course
from ..orm.unit_of_work import DomainObject


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass
