from aioWebWolf.utils.creators.response_creator import create_response


class NotFound:
    async def __call__(self, request):
        return create_response(400, '404 Not Found')
