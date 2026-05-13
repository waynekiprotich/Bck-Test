from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.schemas import user_schema

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/profile")
@jwt_required()
def get_profile():
    """Return the logged-in user's full profile."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200


@users_bp.put("/profile")
@jwt_required()
def update_profile():
    """Update the logged-in user's editable fields."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json(silent=True) or {}

    # Only allow updating safe fields
    if "name" in data:
        name = data["name"].strip()
        if len(name) < 2 or len(name) > 80:
            return jsonify({"error": "Name must be 2–80 characters."}), 400
        user.name = name

    if "bio" in data:
        user.bio = data["bio"].strip()

    if "avatar_url" in data:
        user.avatar_url = data["avatar_url"].strip()

    if "institution_id" in data:
        user.institution_id = data["institution_id"]

    db.session.commit()
    return user_schema.jsonify(user), 200


@users_bp.get("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    """Return a public profile for any user by ID."""
    user = User.query.get_or_404(user_id)
    # Return a limited view (exclude private fields like email)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "points": user.points,
        "rank_tier": user.rank_tier,
        "institution": {
            "id": user.institution.id,
            "name": user.institution.name,
        } if user.institution else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }), 200
