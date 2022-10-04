# get requests
from aioWebWolf.utils.decoder import Decoder


class GetRequests:

    @classmethod
    async def parse_input_data(cls, data: str):
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @classmethod
    async def get_request_params(cls, environ):
        # получаем параметры запроса
        query_bytes: bytes = environ['query_string']
        query_string = query_bytes.decode('UTF-8')

        result = await cls.parse_input_data(query_string)
        request_params = await cls.decode_params(result)
        return request_params

    @classmethod
    async def decode_params(cls, data):
        return await Decoder.get_post_request_data(data)
