from datetime import datetime
from app.extensions import db


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    invite_code = db.Column(db.String(12), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    admin = db.relationship("User", foreign_keys=[admin_id], back_populates="created_groups")
    members = db.relationship(
        "GroupMember",
        back_populates="group",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Group {self.name}>"


class GroupMember(db.Model):
    __tablename__ = "group_members"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships back to both sides
    user = db.relationship("User", back_populates="groups")
    group = db.relationship("Group", back_populates="members")

    def __repr__(self):
        return f"<GroupMember user={self.user_id} group={self.group_id}>"
