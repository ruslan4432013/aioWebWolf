def create_body_response(body: str):
    return {
        'type': 'http.response.body',
        'body': body.encode('utf-8'),
    }
