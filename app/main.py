from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import db
from app.routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)

    # Register Blueprint
    app.register_blueprint(api, url_prefix="/")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
