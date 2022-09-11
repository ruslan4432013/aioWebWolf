import importlib
import json
import os
import socket
from typing import Final

from aioWebWolf.utils.errors.attribute_errors import IncorrectVariable
from aioWebWolf.utils.helpers.check_address import check_address_is_available


def get_module_settings():
    try:
        settings = importlib.import_module('config.settings')

    except ModuleNotFoundError:
        raise ModuleNotFoundError('Не найден модуль config по пути config/settings.py')
    return settings


def check_connection(settings):
    try:
        ip = settings.IP_ADDRESS
        port = settings.PORT
        check_address_is_available(ip, port)
    except socket.error:
        pass
    except AttributeError:
        raise AttributeError('В модуле settings отсутствуют переменные IP_ADDRESS или PORT')


def check_env():
    settings = get_module_settings()

    check_connection(settings)


def setup_env():
    settings = get_module_settings()
    try:
        if type(settings.INSTALLED_APPS) != list:
            raise IncorrectVariable('INSTALLED_APPS должен быть списком')

        INSTALLED_APPS: Final = json.dumps(settings.INSTALLED_APPS)

        os.environ['INSTALLED_APPS'] = INSTALLED_APPS
    except AttributeError:
        raise AttributeError(
            'В модуле settings отсутствует список INSTALLED_APPS, проверьте, что вы в правильной директории')


def get_installed_apps() -> list:
    apps = os.getenv('INSTALLED_APPS')

    if not apps:
        raise AttributeError('В config/settings.py не прописаны приложения в списке INSTALLED_APPS')

    return json.loads(apps)
