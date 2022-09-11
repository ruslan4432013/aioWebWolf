# get requests
class GetRequests:

    @staticmethod
    async def parse_input_data(data: str):
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    async def get_request_params(environ):
        # получаем параметры запроса
        query_bytes: bytes = environ['query_string']
        query_string = query_bytes.decode('UTF-8')

        request_params = await GetRequests.parse_input_data(query_string)
        return request_params
