from quopri import decodestring
import re


class Decoder:

    @staticmethod
    def char_handle(match: re.Match):
        new_string = match.group()
        unicode_string = new_string.replace('&#', '').replace(';', '')
        return chr(int(unicode_string))

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    @classmethod
    async def get_post_request_data(cls, data):
        new_data = {}
        for k, v in data.items():
            val_decode_str = cls.decode_value(v)
            new_data[k] = await cls.decode_unicode_sting(val_decode_str)
        return new_data

    @classmethod
    async def decode_unicode_sting(cls, value: str):
        correct_value = re.sub(r'&#\d+;', cls.char_handle, value)

        return correct_value
