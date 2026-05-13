from app.extensions import db
from app.models.notification import Notification


def notify(user_id: int, ntype: str, message: str) -> Notification:
    """
    Create and persist a notification for a user.

    Args:
        user_id: The recipient user's ID
        ntype:   Notification type e.g. "friend_request", "submission_result", "rank_up"
        message: Human-readable notification text
    """
    notif = Notification(
        user_id=user_id,
        type=ntype,
        message=message,
        is_read=False,
    )
    db.session.add(notif)
    db.session.commit()
    return notif


def get_user_notifications(user_id: int):
    """Return the 50 most recent notifications for a user."""
    return (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )


def mark_read(notification_id: int, user_id: int) -> Notification:
    """
    Mark a notification as read.
    Raises PermissionError if the notification doesn't belong to user_id.
    """
    notif = Notification.query.get_or_404(notification_id)
    if notif.user_id != user_id:
        raise PermissionError("You cannot update another user's notification.")
    notif.is_read = True
    db.session.commit()
    return notif
