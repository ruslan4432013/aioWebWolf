from os import path

from jinja2 import FileSystemLoader, Environment

from aioWebWolf.utils.helpers import get_installed_apps


def render_template_in_bytes(template_name, **kwargs):
    apps = get_installed_apps()

    template_folders = [path.join(app, 'templates') for app in apps]

    template_loader = FileSystemLoader(searchpath=template_folders)

    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    return template.render(**kwargs).encode('UTF-8')
