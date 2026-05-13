from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.group import Group
from app.schemas import group_schema, groups_schema
from app.services.group_service import create_group, join_group, get_user_groups

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


@groups_bp.post("/")
@jwt_required()
def create():
    """Create a new group. The creator is automatically the admin and a member."""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    if not data.get("name", "").strip():
        return jsonify({"error": "Group name is required."}), 400

    try:
        group = create_group(admin_id=user_id, data=data)
        return group_schema.jsonify(group), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@groups_bp.get("/")
@jwt_required()
def list_groups():
    """Return all groups the current user belongs to."""
    user_id = get_jwt_identity()
    user_groups = get_user_groups(user_id)
    return groups_schema.jsonify(user_groups), 200


@groups_bp.post("/join")
@jwt_required()
def join():
    """Join a group using an invite code."""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    invite_code = data.get("invite_code", "").strip().upper()

    if not invite_code:
        return jsonify({"error": "invite_code is required."}), 400

    try:
        group = join_group(user_id=user_id, invite_code=invite_code)
        return group_schema.jsonify(group), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@groups_bp.get("/<int:group_id>")
@jwt_required()
def get_group(group_id):
    """Return a group with all its members."""
    group = Group.query.get_or_404(group_id)
    return group_schema.jsonify(group), 200
