import logging

from flask import Flask
from flask_marshmallow import Marshmallow
from app.routes.game import game_router

from . import settings

PATH_PREFIX = "/api/v1"
logging.basicConfig(
    level=settings.LOGGING_LEVEL,
    format="[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s %(threadName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)
LOG = logging.getLogger(__name__)

application = Flask(__name__)
application.config.from_object(settings)
application.register_blueprint(game_router, url_prefix=f"{PATH_PREFIX}/game")
ma = Marshmallow(application)


@application.route("/")
def index():
    return "Welcome to the game"
