from datetime import datetime
from app.extensions import db


class FriendRequest(db.Model):
    __tablename__ = "friend_requests"

    id = db.Column(db.Integer, primary_key=True)
    
    # both sender and receiver link back to the users table
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    status = db.Column(
        db.Enum("Pending", "Accepted", "Rejected", name="friend_status"),
        default="Pending",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_requests",
    )
    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="recv_requests",
    )

    def __repr__(self):
        return f"<FriendRequest {self.sender_id} -> {self.receiver_id} [{self.status}]>"