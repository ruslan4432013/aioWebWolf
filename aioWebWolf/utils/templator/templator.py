from jinja2 import FileSystemLoader, Environment


def render_template_in_bytes(template_name, **kwargs):
    template_loader = FileSystemLoader(searchpath="main/templates")

    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    return template.render(**kwargs).encode('UTF-8')
