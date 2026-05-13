from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.challenge import Challenge, WeeklyChallenge
from app.schemas import challenge_schema, challenges_schema, weekly_schema
from app.utils.pagination import paginate

challenges_bp = Blueprint("challenges", __name__, url_prefix="/challenges")


@challenges_bp.get("/")
@jwt_required()
def get_challenges():
    """
    Return a paginated list of all challenges.
    Optional filter: ?difficulty=Easy|Medium|Hard
    """
    difficulty = request.args.get("difficulty")
    query = Challenge.query

    if difficulty:
        if difficulty not in ["Easy", "Medium", "Hard"]:
            return jsonify({"error": "difficulty must be Easy, Medium, or Hard"}), 400
        query = query.filter_by(difficulty=difficulty)

    query = query.order_by(Challenge.created_at.desc())
    return jsonify(paginate(query, challenges_schema)), 200


@challenges_bp.get("/practice")
@jwt_required()
def get_practice():
    """Return paginated practice challenges only."""
    query = (
        Challenge.query
        .filter_by(is_practice=True)
        .order_by(Challenge.difficulty, Challenge.created_at)
    )
    return jsonify(paginate(query, challenges_schema)), 200


@challenges_bp.get("/weekly")
@jwt_required()
def get_weekly():
    """Return the currently active weekly challenge."""
    weekly = WeeklyChallenge.query.filter_by(is_active=True).first_or_404(
        description="No active weekly challenge at the moment."
    )
    return weekly_schema.jsonify(weekly), 200


@challenges_bp.get("/<int:challenge_id>")
@jwt_required()
def get_challenge(challenge_id):
    """Return a single challenge with its visible test cases."""
    challenge = Challenge.query.get_or_404(challenge_id)
    return challenge_schema.jsonify(challenge), 200
