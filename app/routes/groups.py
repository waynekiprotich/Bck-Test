from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.group import Group
from app.schemas import group_schema, groups_schema
from app.services.group_service import create_group, join_group, get_user_groups

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


@groups_bp.post("/")
@jwt_required()
def create():
    # allow users to create their own groups (they become the admin automatically)
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
    # get the list of groups the logged-in user has joined
    user_id = get_jwt_identity()
    user_groups = get_user_groups(user_id)
    return groups_schema.jsonify(user_groups), 200


@groups_bp.post("/join")
@jwt_required()
def join():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    
    # normalize the code to uppercase to prevent casing errors
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
    # fetch group details including the member list via the schema
    group = Group.query.get_or_404(group_id)
    return group_schema.jsonify(group), 200