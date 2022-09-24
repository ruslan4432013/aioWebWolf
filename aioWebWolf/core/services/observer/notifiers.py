from .abstractions import Observer


class SmsNotifier(Observer):

    async def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    async def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))
