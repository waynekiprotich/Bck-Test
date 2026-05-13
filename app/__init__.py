from flask import Flask
from app.extensions import db, migrate, jwt, ma
from app.config import get_config


def create_app(env="development"):
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    # Initialise extensions — order matters
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    # Import all models so Flask-Migrate can detect them
    with app.app_context():
        from app.models import (  # noqa: F401
            User, Institution, Challenge, TestCase,
            WeeklyChallenge, Submission, Group,
            GroupMember, FriendRequest, Notification,
        )

    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    # Register error handlers
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)

    # Register middleware
    from app.middleware import register_middleware
    register_middleware(app)

    return app
