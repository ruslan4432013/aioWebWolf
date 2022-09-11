from .views import main, contacts, about

routes = {
    '/': main,
    '/contacts/': contacts,
    '/about/': about
}
