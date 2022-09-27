from abc import ABCMeta, abstractmethod
from sqlite3 import Connection

from aioWebWolf.core.exeptions import RecordNotFoundException, DbCommitException, DbUpdateException, DbDeleteException


class BaseMapper(metaclass=ABCMeta):
    def __init__(self, connection: Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    @property
    @abstractmethod
    def table_name(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass

    def all(self):
        statement = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(statement)
        column_names = [desc_info[0] for desc_info in self.cursor.description]
        result = []

        for values in self.cursor.fetchall():
            obj = self.model(**{column_names[i]: values[i] for i, _ in enumerate(values)})

            result.append(obj)

        return result

    def get_by_id(self, item_id: int | str):
        statement = f'SELECT * FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (item_id,))
        result = self.cursor.fetchone()

        try:
            result_id, name = result
            return self.model(id=result_id, name=name)
        except Exception as e:
            raise RecordNotFoundException(f'record with id={item_id} not found')

    def insert(self, **schema):
        columns = ",".join(schema.keys())
        values = ','.join(schema.values())

        statement = f'INSERT INTO {self.table_name} ({columns}) VALUES (?)'

        self.cursor.execute(statement, (values,))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj, **schema):
        schema = {f'{key}=?': value for key, value in schema.items()}

        columns = ','.join(schema.keys())
        values = ','.join(schema.items())

        statement = f'UPDATE {self.table_name} SET {columns} WHRE id=?'

        self.cursor.execute(statement, (values, obj.id))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.table_name} WHERE id=?'

        self.cursor.execute(statement, (obj.id,))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)
