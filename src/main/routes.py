from .views import Index, Contacts, About, CoursesList, Courses, CreateCourse, CreateCategory, CategoryList,CopyCourse

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/about/': About(),
    '/courses/': Courses(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse(),
}
