# builtins imports
import uvicorn
import sys

sys.path.append('..')

# aioWebWolf imports
from aioWebWolf.app import Application
from aioWebWolf.middlewares import secret_middleware, other_middleware

# local imports
from main.views import main_route
from config.settings import IP_ADDRESS, PORT

middlewares = [secret_middleware, other_middleware]

app = Application(route=main_route, middlewares=middlewares)

if __name__ == "__main__":
    # Адрес и порт обязательно берется из настроек
    uvicorn.run(app, host=IP_ADDRESS, port=PORT)
