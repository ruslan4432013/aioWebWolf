import uvicorn
import sys

sys.path.append('..')

from aioWebWolf.app import Application
from aioWebWolf.middlewares import secret_middleware, other_middleware
from main.routes import routes
from config.settings import IP_ADDRESS, PORT

middlewares = [secret_middleware, other_middleware]

app = Application(routes=routes, middlewares=middlewares)

if __name__ == "__main__":
    # Адрес и порт обязательно берется из настроек
    uvicorn.run(app, host=IP_ADDRESS, port=PORT)
