from aioWebWolf.utils.responses import template_response


async def main(request):
    return template_response('main/index.jinja2')


async def contacts(request):
    return template_response('main/contacts.jinja2')


async def about(request):
    return template_response('main/about.jinja2')
