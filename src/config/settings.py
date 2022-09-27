import os
from pathlib import Path

INSTALLED_APPS = [
    'main'
]

IP_ADDRESS = '127.0.0.1'
PORT = 8000

BASE_DIR = Path(__file__).resolve().parent.parent

DB_NAME = 'project.sqlite'

PATH_TO_DB = os.path.join(BASE_DIR, 'db_core', DB_NAME)



