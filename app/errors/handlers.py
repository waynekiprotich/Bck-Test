from flask import jsonify
from marshmallow import ValidationError


def register_error_handlers(app):
    """Register JSON error handlers for all standard HTTP errors."""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request", "details": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Unauthorised — please log in"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Forbidden — you do not have permission"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": "Unprocessable entity", "details": str(e)}), 422

    @app.errorhandler(429)
    def rate_limited(e):
        return jsonify({"error": "Too many requests — slow down"}), 429

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(ValidationError)
    def marshmallow_validation_error(e):
        """Catch Marshmallow schema validation errors and return 422."""
        return jsonify({"error": "Validation failed", "details": e.messages}), 422
