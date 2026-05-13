from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import notifications_schema, notification_schema
from app.services.notification_service import get_user_notifications, mark_read

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@notifications_bp.get("/")
@jwt_required()
def get_notifications():
    # fetch the recent alerts for the user's dashboard
    user_id = get_jwt_identity()
    notifs = get_user_notifications(user_id)
    
    return notifications_schema.jsonify(notifs), 200


@notifications_bp.put("/<int:notification_id>/read")
@jwt_required()
def mark_as_read(notification_id):
    user_id = get_jwt_identity()
    try:
        notif = mark_read(notification_id=notification_id, user_id=user_id)
        return jsonify({"message": "Notification marked as read.", "id": notif.id}), 200
    
    except PermissionError as e:
        # return a 403 if they try to touch a notification that isn't theirs
        return jsonify({"error": str(e)}), 403