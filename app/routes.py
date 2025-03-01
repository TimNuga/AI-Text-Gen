import openai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app.models import db, User, GeneratedText
from datetime import datetime
from app.config import Config

api = Blueprint("api", __name__)

@api.route("/register", methods=["POST"])
def register():
    """
    Register a new user with a unique username and password.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@api.route("/login", methods=["POST"])
def login():
    """
    Authenticate user and return a JWT token.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate JWT token; cast user.id (int) to string
    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200

@api.route("/generate-text", methods=["POST"])
@jwt_required()
def generate_text():
    """
    Send a prompt to the OpenAI API and store the AI-generated response in the database.
    """
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"message": "Prompt is required"}), 400

    # Get current user ID
    user_id = get_jwt_identity()

    # Using OpenAI's API to generate text
    openai.api_key = Config.OPENAI_API_KEY
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        generated_text = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({"message": f"OpenAI API error: {str(e)}"}), 500

    # Store result in database
    new_generated_text = GeneratedText(
        user_id=user_id,
        prompt=prompt,
        response=generated_text
    )
    db.session.add(new_generated_text)
    db.session.commit()

    return jsonify({
        "id": new_generated_text.id,
        "prompt": prompt,
        "response": generated_text,
        "timestamp": new_generated_text.timestamp
    }), 201

@api.route("/generated-text/<int:text_id>", methods=["GET"])
@jwt_required()
def get_generated_text(text_id):
    """
    Retrieve stored AI-generated text by its ID.
    Only the owner can access it.
    """
    user_id = get_jwt_identity()
    generated_text = GeneratedText.query.get_or_404(text_id)

    if str(generated_text.user_id) != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    return jsonify({
        "id": generated_text.id,
        "prompt": generated_text.prompt,
        "response": generated_text.response,
        "timestamp": generated_text.timestamp
    }), 200

@api.route("/generated-text/<int:text_id>", methods=["PUT"])
@jwt_required()
def update_generated_text(text_id):
    """
    Update stored AI-generated text by its ID.
    Only the owner can update it.
    """
    user_id = get_jwt_identity()
    generated_text = GeneratedText.query.get_or_404(text_id)

    if str(generated_text.user_id) != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    new_prompt = data.get("prompt")
    new_response = data.get("response")

    if new_prompt:
        generated_text.prompt = new_prompt
    if new_response:
        generated_text.response = new_response
    generated_text.timestamp = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "id": generated_text.id,
        "prompt": generated_text.prompt,
        "response": generated_text.response,
        "timestamp": generated_text.timestamp
    }), 200

@api.route("/generated-text/<int:text_id>", methods=["DELETE"])
@jwt_required()
def delete_generated_text(text_id):
    """
    Delete stored AI-generated text by its ID.
    Only the owner can delete it.
    """
    user_id = get_jwt_identity()
    generated_text = GeneratedText.query.get_or_404(text_id)

    if str(generated_text.user_id) != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(generated_text)
    db.session.commit()

    return jsonify({"message": f"Generated text with ID {text_id} deleted"}), 200
