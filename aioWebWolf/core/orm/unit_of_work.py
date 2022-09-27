from __future__ import annotations
import threading


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj, schema):
        self.new_objects.append({'obj': obj, 'schema': schema})

    def register_dirty(self, obj, schema):
        self.dirty_objects.append({'obj': obj, 'schema': schema})

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    @classmethod
    def new_current(cls):
        cls.set_current(cls())

    @classmethod
    def get_current(cls) -> UnitOfWork:
        return cls.current.unit_of_work

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    def insert_new(self):
        for obj in self.new_objects:
            print(obj)
            self.MapperRegistry.get_mapper(obj['obj']).insert(
                **obj['schema'])

        self.new_objects.clear()

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.MapperRegistry.get_mapper(obj['obj']).insert(
                obj['obj'], **obj['schema'])

        self.dirty_objects.clear()

    def delete_removed(self):
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

        self.removed_objects.clear()


class DomainObject:
    def mark_new(self, schema):
        UnitOfWork.get_current().register_new(self, schema)

    def mark_dirty(self, schema):
        UnitOfWork.get_current().register_dirty(self, schema)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
