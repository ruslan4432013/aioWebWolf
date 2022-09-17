from ..templator import render_template
from ..creators import create_response


def template_response(template_name, **kwargs):
    template_body = render_template(template_name, **kwargs)
    return create_response(200, template_body)
