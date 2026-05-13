from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import user_schema, friend_schema, friends_schema
from app.services.friend_service import (
    send_friend_request,
    update_friend_status,
    get_friends,
)

friends_bp = Blueprint("friends", __name__, url_prefix="/friends")


@friends_bp.post("/request")
@jwt_required()
def send_request():
    # grab the sender's id directly from their active jwt token
    sender_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    receiver_id = data.get("receiver_id")

    if not receiver_id:
        return jsonify({"error": "receiver_id is required."}), 400

    try:
        req = send_friend_request(sender_id=sender_id, receiver_id=int(receiver_id))
        return jsonify({"message": "Friend request sent.", "id": req.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@friends_bp.put("/<int:request_id>/status")
@jwt_required()
def update_status(request_id):
    # frontend should pass either 'Accepted' or 'Rejected' in the body
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    new_status = data.get("status", "")

    if new_status not in ["Accepted", "Rejected"]:
        return jsonify({"error": "status must be 'Accepted' or 'Rejected'."}), 400

    try:
        req = update_friend_status(request_id=request_id, user_id=user_id, new_status=new_status)
        return jsonify({"message": f"Friend request {new_status.lower()}.", "id": req.id}), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@friends_bp.get("/")
@jwt_required()
def list_friends():
    user_id = get_jwt_identity()
    accepted = get_friends(user_id)

    # figure out which person in the relationship is the "other" user
    friends_list = []
    for req in accepted:
        other = req.receiver if req.sender_id == user_id else req.sender
        friends_list.append(user_schema.dump(other))

    return jsonify(friends_list), 200