from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import user_blueprint
from app.models import db
from app.repositories.user_repository import UserRepository

user_repo = UserRepository(db.session)

@user_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = int(get_jwt_identity())
    user = user_repo.find_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200
