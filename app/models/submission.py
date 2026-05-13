from datetime import datetime
from app.extensions import db

SUBMISSION_STATUSES = [
    "Pending",
    "Running",
    "Accepted",
    "Wrong Answer",
    "Runtime Error",
    "Compilation Error",
    "Time Limit Exceeded",
]

SUPPORTED_LANGUAGES = ["python", "javascript"]


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    language = db.Column(
        db.Enum("python", "javascript", name="submission_language"),
        nullable=False,
    )
    code = db.Column(db.Text, nullable=False)
    stdout = db.Column(db.Text)
    stderr = db.Column(db.Text)
    execution_time = db.Column(db.Float)       # seconds
    memory_used = db.Column(db.Float)          # MB
    status = db.Column(db.String(30), default="Pending", nullable=False)
    score = db.Column(db.Integer, default=0)
    passed_tests = db.Column(db.Integer, default=0)
    total_tests = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="submissions")
    challenge = db.relationship("Challenge", back_populates="submissions")

    def __repr__(self):
        return f"<Submission user={self.user_id} challenge={self.challenge_id} status={self.status}>"
