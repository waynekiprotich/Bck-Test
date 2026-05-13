from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.services.auth_service import check_email_exists, register_user, login_user
from app.models.user import User
from app.schemas import user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/check-email")
def check_email():
    # first step for the frontend flow: check if we should show the login or register screen next
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    
    if not email:
        return jsonify({"error": "Email is required."}), 400

    exists = check_email_exists(email)
    return jsonify({"exists": exists}), 200


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    try:
        result = register_user(data)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.messages}), 422
    except ValueError as e:
        return jsonify({"error": str(e)}), 409  # conflict if email is already taken


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    try:
        result = login_user(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.get("/me")
@jwt_required()
def me():
    # locked down route to get the current user's profile using their jwt token
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200