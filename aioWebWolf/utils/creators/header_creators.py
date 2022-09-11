def create_http_headers(status: int):
    return {
        'type': 'http.response.start',
        'status': status,
        'headers': [
            [b'content-type', b'text/html'],
        ]
    }



