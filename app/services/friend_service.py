from app.extensions import db
from app.models.friend import FriendRequest
from app.services.notification_service import notify


def send_friend_request(sender_id: int, receiver_id: int) -> FriendRequest:
    """
    Send a friend request from sender to receiver.
    Raises ValueError if invalid (self-request or duplicate).
    """
    if sender_id == receiver_id:
        raise ValueError("You cannot send a friend request to yourself.")

    existing = FriendRequest.query.filter(
        (
            (FriendRequest.sender_id == sender_id) &
            (FriendRequest.receiver_id == receiver_id)
        ) | (
            (FriendRequest.sender_id == receiver_id) &
            (FriendRequest.receiver_id == sender_id)
        ),
        FriendRequest.status.in_(["Pending", "Accepted"]),
    ).first()

    if existing:
        raise ValueError("A friend request or friendship already exists.")

    req = FriendRequest(sender_id=sender_id, receiver_id=receiver_id)
    db.session.add(req)
    db.session.commit()

    notify(
        user_id=receiver_id,
        ntype="friend_request",
        message="You have a new friend request!",
    )
    return req


def update_friend_status(request_id: int, user_id: int, new_status: str) -> FriendRequest:
    """
    Accept or reject a friend request.
    Only the receiver may change the status.
    """
    req = FriendRequest.query.get_or_404(request_id)

    if req.receiver_id != user_id:
        raise PermissionError("Only the recipient can accept or reject a friend request.")

    if req.status != "Pending":
        raise ValueError("This request has already been responded to.")

    req.status = new_status
    db.session.commit()

    if new_status == "Accepted":
        notify(
            user_id=req.sender_id,
            ntype="friend_accepted",
            message="Your friend request was accepted!",
        )
    return req


def get_friends(user_id: int):
    """Return all accepted FriendRequest rows involving this user."""
    return FriendRequest.query.filter(
        (
            (FriendRequest.sender_id == user_id) |
            (FriendRequest.receiver_id == user_id)
        ),
        FriendRequest.status == "Accepted",
    ).all()
