from app.extensions import db
from app.models.notification import Notification


def notify(user_id: int, ntype: str, message: str) -> Notification:
    # create a new notification for a specific event (like a rank up or friend request)
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
    # only grab the 50 most recent so we don't overload the frontend
    return (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )


def mark_read(notification_id: int, user_id: int) -> Notification:
    notif = Notification.query.get_or_404(notification_id)
    
    # prevent users from trying to mark someone else's notifications as read
    if notif.user_id != user_id:
        raise PermissionError("You cannot update another user's notification.")
    
    notif.is_read = True
    db.session.commit()
    return notif