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
    # standard global ranking based on total points accumulated
    query = get_global_leaderboard_query()
    return jsonify(paginate(query, users_schema)), 200


@leaderboard_bp.get("/groups")
@jwt_required()
def groups_leaderboard():
    # rank groups by adding up the points of everyone in them
    results = get_group_leaderboard()
    
    leaderboard_data = [
        {
            "group": group_schema.dump(g),
            "total_points": int(pts),
            "member_count": int(count),
        }
        for g, pts, count in results
    ]
    
    return jsonify({
        "data": leaderboard_data, 
        "count": len(leaderboard_data)
    }), 200


@leaderboard_bp.get("/weekly/<int:week_number>")
@jwt_required()
def weekly_leaderboard(week_number):
    # filter rankings for a specific weekly challenge event
    results, weekly = get_weekly_leaderboard(week_number)
    
    rankings = [
        {
            "user": user_schema.dump(u),
            "best_score": int(score),
        }
        for u, score in results
    ]
    
    return jsonify({
        "week_number": weekly.week_number,
        "challenge_id": weekly.challenge_id,
        "data": rankings,
    }), 200