import asyncio
from aioWebWolf.utils.helpers.environment import check_env, setup_env
from aioWebWolf.utils.requests_handlers import GetRequests, PostRequests
from aioWebWolf.views import not_found_404_view


class Application:
    def __init__(self, routes, middlewares=None):
        check_env()
        setup_env()

        if middlewares is None:
            middlewares = []
        self.routes = routes
        self.middlewares = middlewares

    def get_view(self, path):
        if not path.endswith('/'):
            path += '/'

        view = not_found_404_view

        if path in self.routes:
            view = self.routes[path]

        return view

    async def start_middleware_handling(self, request):
        tasks = [asyncio.create_task(middleware(request)) for middleware in self.middlewares]
        await asyncio.wait(tasks)

    @staticmethod
    async def send_response(send, view, request):
        headers, body = await view(request)

        await send(headers)
        await send(body)

    async def __call__(self, scope, receive, send):
        """
        :param scope: Словарь, содержащий информацию о входящем соединении
        :param receive: Канал, по которому будут приниматься входящие сообщения с сервера.
        :param send:  Канал, по которому отправляются исходящие сообщения на сервер.
        """
        request = {}
        if scope['type'] == 'http':
            if scope['method'] == 'GET':
                params = await GetRequests.get_request_params(scope)
                request['request_params'] = params
                params and print(f'Нам пришли GET-параметры: {params}')
            else:
                params = await PostRequests.get_request_params(receive=receive)
                request['data'] = params
                print(f'Нам пришёл post-запрос: {params}')

            path = scope['path']
            view = self.get_view(path)

            await self.start_middleware_handling(request)
            await self.send_response(send, view, request)
