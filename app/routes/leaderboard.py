from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.schemas import user_schema, users_schema, group_schema
from app.services.leaderboard_service import (
    get_global_leaderboard_query,
    get_group_leaderboard,
    get_weekly_leaderboard,
)
from app.utils.pagination import paginate

leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@leaderboard_bp.get("/")
@jwt_required()
def global_leaderboard():
    """All users ranked by total points (paginated)."""
    query = get_global_leaderboard_query()
    return jsonify(paginate(query, users_schema)), 200


@leaderboard_bp.get("/groups")
@jwt_required()
def groups_leaderboard():
    """All groups ranked by sum of members' points."""
    results = get_group_leaderboard()
    data = [
        {
            "group": group_schema.dump(group),
            "total_points": int(total_points),
            "member_count": int(member_count),
        }
        for group, total_points, member_count in results
    ]
    return jsonify({"data": data, "count": len(data)}), 200


@leaderboard_bp.get("/weekly/<int:week_number>")
@jwt_required()
def weekly_leaderboard(week_number):
    """Users ranked by best score on a specific weekly challenge."""
    results, weekly = get_weekly_leaderboard(week_number)
    data = [
        {
            "user": user_schema.dump(user),
            "best_score": int(best_score),
        }
        for user, best_score in results
    ]
    return jsonify({
        "week_number": weekly.week_number,
        "challenge_id": weekly.challenge_id,
        "data": data,
    }), 200
