from aioWebWolf.views import NotFound


class AppRoute:
    routes = {}

    def all_requests(self, url: str):
        def decorator(cls):
            path = url

            if not path.endswith('/'):
                path += '/'

            self.routes[path] = cls()

            return cls

        return decorator

    def get_view(self, route: str):

        path = route
        if not path.endswith('/'):
            path += '/'

        if path in self.routes:
            return self.routes[path]
        return NotFound()
