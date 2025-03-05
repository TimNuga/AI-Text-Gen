from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.validation import GenerateTextSchema
from app.models import db
from app.repositories.generated_text_repository import GeneratedTextRepository
from app.providers.openai_provider import OpenAIProvider
from app.services.ai_service import AIService
from app.routes import generate_text_blueprint

gen_text_repo = GeneratedTextRepository(db.session)
ai_service = AIService(OpenAIProvider())

@generate_text_blueprint.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify(err.messages), 422

@generate_text_blueprint.route("/generate-text", methods=["POST"])
@jwt_required()
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt")
    GenerateTextSchema().load(data)
    current_user_id = int(get_jwt_identity())
    
    try:
        result = ai_service.generate_text(prompt)
    
        new_text = gen_text_repo.create_text(current_user_id, prompt, result)
        return jsonify({
            "id": new_text.id,
            "prompt": new_text.prompt,
            "response": new_text.response,
            "timestamp": new_text.timestamp
        }), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400

@generate_text_blueprint.route("/generated-text/<int:text_id>", methods=["GET"])
@jwt_required()
def get_generated_text(text_id):
    current_user_id = int(get_jwt_identity())
    gen_text = gen_text_repo.find_by_id(text_id)
    if not gen_text:
        return jsonify({"message": "Not found"}), 404
    if gen_text.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    return jsonify({
        "id": gen_text.id,
        "prompt": gen_text.prompt,
        "response": gen_text.response,
        "timestamp": gen_text.timestamp
    }), 200

@generate_text_blueprint.route("/generated-text/<int:text_id>", methods=["PUT"])
@jwt_required()
def update_generated_text(text_id):
    current_user_id = int(get_jwt_identity())
    gen_text = gen_text_repo.find_by_id(text_id)
    if not gen_text:
        return jsonify({"message": "Not found"}), 404
    if gen_text.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    new_prompt = data.get("prompt")
    new_response = data.get("response")
    
    updated = gen_text_repo.update_text(gen_text, new_prompt, new_response)
    return jsonify({
        "id": updated.id,
        "prompt": updated.prompt,
        "response": updated.response,
        "timestamp": updated.timestamp
    }), 200

@generate_text_blueprint.route("/generated-text/<int:text_id>", methods=["DELETE"])
@jwt_required()
def delete_generated_text(text_id):
    current_user_id = int(get_jwt_identity())
    gen_text = gen_text_repo.find_by_id(text_id)
    if not gen_text:
        return jsonify({"message": "Not found"}), 404
    if gen_text.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    gen_text_repo.delete_text(gen_text)
    return jsonify({"message": f"Deleted text with ID {text_id}"}), 200
