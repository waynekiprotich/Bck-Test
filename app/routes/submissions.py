from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.challenge import Challenge
from app.models.user import User
from app.models.submission import Submission
from app.schemas import submission_schema, submissions_schema
from app.services.scoring_service import evaluate_submission, update_user_points
from app.services.notification_service import notify
from app.utils.pagination import paginate
from app.utils.rate_limiter import rate_limit

submissions_bp = Blueprint("submissions", __name__)


@submissions_bp.post("/submit-code")
@jwt_required()
def submit_code():
    user_id = get_jwt_identity()

    # stop users from spamming the piston api (max 10 tries per minute)
    if rate_limit(f"submit:{user_id}", max_calls=10, window_seconds=60):
        return jsonify({"error": "Too many submissions. Please wait a moment."}), 429

    data = request.get_json(silent=True) or {}
    challenge_id = data.get("challenge_id")
    language = data.get("language", "").lower()
    code = data.get("code", "").strip()

    # verify we have everything we need to run the code
    if not challenge_id:
        return jsonify({"error": "challenge_id is required."}), 400
    if language not in ["python", "javascript"]:
        return jsonify({"error": "language must be 'python' or 'javascript'."}), 400
    if not code:
        return jsonify({"error": "code cannot be empty."}), 400

    challenge = Challenge.query.get_or_404(challenge_id)
    test_cases = challenge.test_cases.all()

    if not test_cases:
        return jsonify({"error": "This challenge has no test cases yet."}), 400

    # save the submission row as 'Running' so the user doesn't think it's stuck if Piston is slow
    sub = Submission(
        user_id=user_id,
        challenge_id=challenge_id,
        language=language,
        code=code,
        status="Running",
        total_tests=len(test_cases),
    )
    db.session.add(sub)
    db.session.commit()

    # trigger the evaluation service to run against Piston
    result = evaluate_submission(sub, challenge, test_cases)
    db.session.commit()

    # add the points to the user's profile
    user = User.query.get(user_id)
    update_user_points(user, result["score"])

    # send a notification to the user's dashboard with their results
    notify(
        user_id=user_id,
        ntype="submission_result",
        message=(
            f"Your submission for '{challenge.title}': {result['status']} "
            f"({result['passed_tests']}/{result['total_tests']} tests passed, "
            f"{result['score']} pts earned)"
        ),
    )

    return submission_schema.jsonify(sub), 201


@submissions_bp.get("/results")
@jwt_required()
def get_results():
    # fetch the user's past attempts (paginated so the history page loads fast)
    user_id = get_jwt_identity()
    query = (
        Submission.query
        .filter_by(user_id=user_id)
        .order_by(Submission.created_at.desc())
    )
    return jsonify(paginate(query, submissions_schema)), 200


@submissions_bp.get("/results/<int:submission_id>")
@jwt_required()
def get_result(submission_id):
    user_id = get_jwt_identity()
    sub = Submission.query.get_or_404(submission_id)
    
    # check that the user isn't trying to peek at someone else's code
    if sub.user_id != user_id:
        return jsonify({"error": "Forbidden — this is not your submission."}), 403
        
    return submission_schema.jsonify(sub), 200