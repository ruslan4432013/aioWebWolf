from aioWebWolf.utils.creators.response_creator import create_response


async def not_found_404_view(request):
    return create_response(400, b'404 Not Found')
