from aioWebWolf.utils.decoder import Decoder
from aioWebWolf.utils.helpers import read_body


class PostRequests:

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
    async def get_asgi_input_data(receive) -> bytes:

        data = await read_body(receive)

        return data

    @classmethod
    async def parse_asgi_input_data(cls, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')

            # собираем их в словарь
            result = await cls.parse_input_data(data_str)
        return result

    @classmethod
    async def get_request_params(cls, receive):
        # получаем данные
        data = await cls.get_asgi_input_data(receive)
        # превращаем данные в словарь
        data = await cls.parse_asgi_input_data(data)

        data = await Decoder.get_post_request_data(data)
        return data
