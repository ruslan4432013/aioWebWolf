class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = None

        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name is None:
            raise AttributeError('Атрибут name отсутствует')

        if name not in cls.__instance:
            cls.__instance[name] = super().__call__(*args, **kwargs)

        return cls.__instance[name]


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance
