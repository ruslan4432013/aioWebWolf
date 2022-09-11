from aioWebWolf.utils.responses import template_response


async def main(request):
    print(request)
    return template_response('index.html')


async def contacts(request):
    return template_response('contacts.html')


async def about(request):
    return template_response('about.html')
