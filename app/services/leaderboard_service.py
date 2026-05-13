from sqlalchemy import func
from app.extensions import db
from app.models.user import User
from app.models.group import Group, GroupMember
from app.models.submission import Submission
from app.models.challenge import WeeklyChallenge


def get_global_leaderboard_query():
    """Return a SQLAlchemy query of users ordered by points descending."""
    return User.query.order_by(User.points.desc())


def get_group_leaderboard():
    """
    Return groups ranked by the sum of their members' points.

    Uses a subquery to aggregate per-group, then joins to Group.
    Returns a list of (Group, total_points, member_count) tuples.
    """
    # Subquery: for each group, sum member points + count members
    group_scores = (
        db.session.query(
            GroupMember.group_id,
            func.sum(User.points).label("total_points"),
            func.count(User.id).label("member_count"),
        )
        .join(User, User.id == GroupMember.user_id)
        .group_by(GroupMember.group_id)
        .subquery()
    )

    # Main query: join groups with the aggregated subquery
    results = (
        db.session.query(
            Group,
            group_scores.c.total_points,
            group_scores.c.member_count,
        )
        .join(group_scores, Group.id == group_scores.c.group_id)
        .order_by(group_scores.c.total_points.desc())
        .all()
    )
    return results


def get_weekly_leaderboard(week_number: int):
    """
    Return users ranked by their best score on the active weekly challenge.
    Only accepted submissions within the weekly window count.
    """
    weekly = WeeklyChallenge.query.filter_by(
        week_number=week_number, is_active=True
    ).first_or_404()

    best_scores = (
        db.session.query(
            Submission.user_id,
            func.max(Submission.score).label("best_score"),
        )
        .filter(
            Submission.challenge_id == weekly.challenge_id,
            Submission.created_at >= weekly.start_date,
            Submission.created_at <= weekly.end_date,
            Submission.status == "Accepted",
        )
        .group_by(Submission.user_id)
        .subquery()
    )

    results = (
        db.session.query(User, best_scores.c.best_score)
        .join(best_scores, User.id == best_scores.c.user_id)
        .order_by(best_scores.c.best_score.desc())
        .all()
    )
    return results, weekly
