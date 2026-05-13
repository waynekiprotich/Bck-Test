from datetime import datetime
from app.extensions import db


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(
        db.Enum("Easy", "Medium", "Hard", name="difficulty_level"),
        nullable=False,
    )
    starter_code_python = db.Column(db.Text)
    starter_code_javascript = db.Column(db.Text)
    is_practice = db.Column(db.Boolean, default=True, nullable=False)
    points_reward = db.Column(db.Integer, nullable=False)
    time_limit = db.Column(db.Integer, default=5000) 
    memory_limit = db.Column(db.Integer, default=128) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # table relationships
    test_cases = db.relationship(
        "TestCase",
        back_populates="challenge",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    submissions = db.relationship(
        "Submission",
        back_populates="challenge",
    )
    weekly_challenges = db.relationship(
        "WeeklyChallenge",
        back_populates="challenge",
    )

    def __repr__(self):
        return f"<Challenge {self.slug}>"


class TestCase(db.Model):
    __tablename__ = "test_cases"

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False
    )
    input_data = db.Column(db.Text)
    expected_output = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    challenge = db.relationship("Challenge", back_populates="test_cases")

    def __repr__(self):
        return f"<TestCase challenge={self.challenge_id} hidden={self.is_hidden}>"


class WeeklyChallenge(db.Model):
    __tablename__ = "weekly_challenges"

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False
    )
    week_number = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    challenge = db.relationship("Challenge", back_populates="weekly_challenges")

    def __repr__(self):
        return f"<WeeklyChallenge week={self.week_number} active={self.is_active}>"