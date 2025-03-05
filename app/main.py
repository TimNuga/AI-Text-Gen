import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)


    db.init_app(app)
    jwt = JWTManager(app)

    # Importing the separate blueprints
    from app.routes import auth_blueprint, user_blueprint, generate_text_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(generate_text_blueprint)  # route definitions already contain /generate-text

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("An uncaught exception occurred")
        return jsonify({"message": f"Internal server error, {e}"}), 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
