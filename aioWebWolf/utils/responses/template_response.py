from ..templator import render_template_in_bytes
from ..creators import create_response


def template_response(template_name, **kwargs):
    template_body = render_template_in_bytes(template_name, **kwargs)
    return create_response(200, template_body)
