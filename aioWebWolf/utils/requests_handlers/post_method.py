from quopri import decodestring
import re

from aioWebWolf.utils.helpers import read_body


class Decoder:

    @staticmethod
    def char_handle(match: re.Match):
        new_string = match.group()
        unicode_string = new_string.replace('&#', '').replace(';', '')
        return chr(int(unicode_string))

    @classmethod
    async def decode_value(cls, data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = await cls.decode_unicode_sting(val_decode_str)
        return new_data

    @classmethod
    async def decode_unicode_sting(cls, value: str):
        correct_value = re.sub(r'&#\d+;', cls.char_handle, value)

        return correct_value


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

        data = await Decoder.decode_value(data)
        return data
