from app.routes.auth import auth_bp
from app.routes.users import users_bp
from app.routes.institutions import institutions_bp
from app.routes.challenges import challenges_bp
from app.routes.submissions import submissions_bp
from app.routes.groups import groups_bp
from app.routes.friends import friends_bp
from app.routes.leaderboard import leaderboard_bp
from app.routes.notifications import notifications_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(institutions_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(submissions_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(friends_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(notifications_bp)
