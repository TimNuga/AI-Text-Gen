from flask import request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.validation import RegisterSchema, LoginSchema
from app.models import db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.routes import auth_blueprint

user_repo = UserRepository(db.session)
user_service = UserService(user_repo)

@auth_blueprint.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify(err.messages), 422

@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    RegisterSchema().load(data)
    
    try:
        user_service.register_user(data["username"], data["password"])
        return jsonify({"message": "User registered"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    LoginSchema().load(data)
    
    user = user_service.verify_credentials(data["username"], data["password"])
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200
