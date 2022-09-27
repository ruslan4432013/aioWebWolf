import os
from sqlite3 import connect

from aioWebWolf.core.orm.mapper import BaseMapper
from aioWebWolf.core.site_builders.abstractions import Category
from aioWebWolf.core.site_builders.models import Student


class StudentMapper(BaseMapper):
    table_name = 'students'
    model = Student


class CategoryMapper(BaseMapper):
    table_name = 'categories'
    model = Category


connection = connect(os.getenv('PATH_TO_DB', 'project.sqlite'))


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name) -> BaseMapper:
        return MapperRegistry.mappers[name](connection)
