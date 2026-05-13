from flask import request, jsonify


def register_middleware(app):
    """Register before/after request hooks."""

    @app.before_request
    def log_request():
        """Log every incoming request method and path."""
        app.logger.info(f"→ {request.method} {request.path} from {request.remote_addr}")

    @app.before_request
    def handle_preflight():
        """Return 200 for OPTIONS preflight requests (required by browsers for CORS)."""
        if request.method == "OPTIONS":
            response = jsonify({})
            response.status_code = 200
            return response

    @app.after_request
    def add_cors_headers(response):
        """
        Allow the React frontend to call this API.
        In production, replace '*' with your actual frontend URL.
        """
        allowed_origins = [
            "http://localhost:5173",          # Vite dev server
            "http://localhost:3000",          # CRA dev server
        ]

        origin = request.headers.get("Origin", "")
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            # Fallback for development — remove in strict production
            response.headers["Access-Control-Allow-Origin"] = "*"

        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response
