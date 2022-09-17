import asyncio


async def secret_middleware(request):
    request['secret'] = 'some secret'


async def other_middleware(request):
    request['key'] = 'value'
