def create_body_response(body: bytes):
    return {
        'type': 'http.response.body',
        'body': body,
    }
