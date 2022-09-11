from .body_creators import create_body_response
from .header_creators import create_http_headers


def create_response(status: int, body: bytes):
    return create_http_headers(status), create_body_response(body)
