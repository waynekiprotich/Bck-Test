from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def jwt_required_user(fn):
    """
    Decorator that verifies JWT and injects the current User object
    as the first argument to the route function.

    Usage:
        @app.get("/profile")
        @jwt_required_user
        def profile(current_user):
            return user_schema.jsonify(current_user)
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        from app.models.user import User
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({"error": "User not found"}), 404
        return fn(current_user, *args, **kwargs)
    return wrapper
