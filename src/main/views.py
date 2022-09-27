from aioWebWolf.core import Engine, Logger, Debugger
from aioWebWolf.core.orm.unit_of_work import UnitOfWork
from aioWebWolf.core.route.route import AppRoute
from aioWebWolf.core.services.cbv.base_view import ListView, CreateView
from aioWebWolf.core.services.observer.notifiers import SmsNotifier, EmailNotifier
from aioWebWolf.core.services.serializer import BaseSerializer
from aioWebWolf.core.site_builders.abstractions import Category
from aioWebWolf.core.site_builders.model_mappers import MapperRegistry, CategoryMapper
from aioWebWolf.utils import create_response
from aioWebWolf.utils.responses import template_response

site = Engine()
logger = Logger('main')

main_route = AppRoute()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@main_route.all_requests(url='/')
class Index:
    @Debugger(name='Index')
    async def __call__(self, request):
        return template_response('main/index.jinja2')


@main_route.all_requests(url='/courses')
class Courses:
    @Debugger(name='Courses')
    async def __call__(self, request):
        category = MapperRegistry.get_current_mapper('category').all()
        return template_response('main/course.jinja2', objects_list=category)


@main_route.all_requests(url='/about')
class About:
    @Debugger(name='About')
    async def __call__(self, request):
        return template_response('main/about.jinja2')


@main_route.all_requests(url='/contacts')
class Contacts:
    @Debugger(name='Contacts')
    async def __call__(self, request):
        return template_response('main/contacts.jinja2')


@main_route.all_requests(url='/courses-list')
class CoursesList:
    @Debugger(name='CoursesList')
    async def __call__(self, request):
        logger.log('Список курсов')
        try:
            category_id = int(request['request_params']['id'])
            category = MapperRegistry.get_current_mapper('category').get_by_id(category_id)
            context = dict(
                objects_list=category.courses,
                name=category.name,
                id=category_id
            )

            return template_response('main/course_list.jinja2', **context)
        except KeyError:
            return create_response(200, 'No courses have been added yet')


@main_route.all_requests(url='/create-course')
class CreateCourse:
    category_id = -1

    @Debugger(name='CreateCourse')
    async def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            category = None
            if self.category_id != -1:
                category = MapperRegistry.get_current_mapper('category').get_by_id(self.category_id)
                course = site.create_course('record', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            context = dict(
                objects_list=category.courses,
                name=category.name,
                id=category.id
            )
            return template_response('main/course_list.jinja2', **context)

        else:
            try:
                self.category_id = int(request['request_params']['id'])

                category = MapperRegistry.get_current_mapper('category').get_by_id(self.category_id)

                return template_response('main/create_course.jinja2',
                                         name=category.name,
                                         id=category.id)
            except KeyError:
                return create_response(200, 'No courses have been added yet')


@main_route.all_requests(url='/create-category')
class CategoriesCreateView(CreateView):
    template_name = 'main/create_category.jinja2'

    async def create_obj(self, data: dict):
        name = data.get('name')

        new_category = site.create_category()

        site.categories.append(new_category)

        schema = {'name': name}
        new_category.mark_new(schema)
        UnitOfWork.get_current().commit()


@main_route.all_requests(url='/category-list')
class CategoryList(ListView):
    template_name = 'main/category_list.jinja2'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


@main_route.all_requests(url='/copy-course')
class CopyCourse:
    @Debugger(name='CopyCourse')
    async def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
            else:
                raise Exception('Нет такого курса, что-то не так')

            return template_response('main/course_list.jinja2',
                                     objects_list=site.courses,
                                     name=new_course.category.name)
        except KeyError:
            return create_response(200, 'No courses have been added yet')


@main_route.all_requests(url='/student-list')
class StudentListView(ListView):
    template_name = 'main/student_list.jinja2'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@main_route.all_requests(url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'main/create_student.jinja2'

    async def create_obj(self, data: dict):
        name: str = data['name']
        new_obj = site.create_user('student')

        site.students.append(new_obj)
        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


@main_route.all_requests(url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'main/add_student.jinja2'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    async def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        await course.add_student(student)


@main_route.all_requests(url='/api/')
class CourseApi:
    @Debugger(name='CourseApi')
    async def __call__(self, request):
        return create_response(200, BaseSerializer(site.courses).save())
