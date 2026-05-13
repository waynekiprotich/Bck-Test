from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.schemas import user_schema

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/profile")
@jwt_required()
def get_profile():
    # grab the current logged-in user's data for the settings or profile page
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200


@users_bp.put("/profile")
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json(silent=True) or {}

    # validation check: don't let them set a name that's too short or too long
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

    # save changes to the database
    db.session.commit()
    return user_schema.jsonify(user), 200


@users_bp.get("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # public profile view: we skip the email and other private fields for safety
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