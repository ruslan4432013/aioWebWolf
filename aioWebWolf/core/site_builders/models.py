from . import User, Course


class Teacher(User):
    pass


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass
