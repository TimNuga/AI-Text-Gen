from flask import Blueprint

auth_blueprint = Blueprint("auth_api", __name__)
user_blueprint = Blueprint("user_api", __name__)
generate_text_blueprint = Blueprint("generate_text_api", __name__)

from app.routes.auth_routes import *           # registers endpoints on auth_blueprint
from app.routes.user_routes import *           # registers endpoints on user_blueprint
from app.routes.generated_text_routes import * # registers endpoints on generate_text_blueprint
