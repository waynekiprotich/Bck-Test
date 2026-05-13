from marshmallow import fields, validate, validates, ValidationError
from app.extensions import ma
from app.models.user import User, Institution
from app.models.challenge import Challenge, TestCase, WeeklyChallenge
from app.models.submission import Submission
from app.models.group import Group, GroupMember
from app.models.friend import FriendRequest
from app.models.notification import Notification


# ─── Institution ──────────────────────────────────────────────────────────────

class InstitutionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Institution
        load_instance = True

    type = fields.Str(validate=validate.OneOf(["University", "Bootcamp"]))


# ─── User ─────────────────────────────────────────────────────────────────────

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        # Never expose the password hash
        exclude = ("password_hash",)

    # Input validation
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(
        load_only=True,   # never serialised in output
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters."),
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=80, error="Name must be 2–80 characters."),
    )

    # Nested: pull institution name into user response
    institution = ma.Nested(InstitutionSchema, only=("id", "name", "type"), dump_only=True)


# ─── Test Case ────────────────────────────────────────────────────────────────

class TestCaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestCase
        load_instance = True
        # is_hidden kept server-side; expected_output never revealed to students
        exclude = ("expected_output",)


class TestCaseAdminSchema(ma.SQLAlchemyAutoSchema):
    """Full schema for seeding / admin use — includes expected_output."""
    class Meta:
        model = TestCase
        load_instance = True


# ─── Challenge ────────────────────────────────────────────────────────────────

class ChallengeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Challenge
        load_instance = True

    difficulty = fields.Str(
        validate=validate.OneOf(
            ["Easy", "Medium", "Hard"],
            error="Difficulty must be Easy, Medium, or Hard.",
        )
    )
    # Return visible test cases only (is_hidden=False)
    test_cases = ma.Nested(TestCaseSchema, many=True, dump_only=True)


# ─── Weekly Challenge ─────────────────────────────────────────────────────────

class WeeklyChallengeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeeklyChallenge
        load_instance = True

    challenge = ma.Nested(ChallengeSchema, dump_only=True)


# ─── Submission ───────────────────────────────────────────────────────────────

class SubmissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Submission
        load_instance = True

    language = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["python", "javascript"],
            error="Only Python or JavaScript is supported.",
        ),
    )
    code = fields.Str(required=True, validate=validate.Length(min=1, error="Code cannot be empty."))

    # Nested references (dump only — set by the server)
    user = ma.Nested(UserSchema, only=("id", "name", "rank_tier"), dump_only=True)
    challenge = ma.Nested(ChallengeSchema, only=("id", "title", "difficulty"), dump_only=True)


# ─── Group ────────────────────────────────────────────────────────────────────

class GroupMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupMember
        load_instance = True

    user = ma.Nested(UserSchema, only=("id", "name", "points", "rank_tier"), dump_only=True)


class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        load_instance = True

    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100, error="Group name must be 3–100 characters."),
    )
    members = ma.Nested(GroupMemberSchema, many=True, dump_only=True)
    admin = ma.Nested(UserSchema, only=("id", "name"), dump_only=True)


# ─── Friend Request ───────────────────────────────────────────────────────────

class FriendRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FriendRequest
        load_instance = True

    sender = ma.Nested(UserSchema, only=("id", "name", "avatar_url"), dump_only=True)
    receiver = ma.Nested(UserSchema, only=("id", "name", "avatar_url"), dump_only=True)
    status = fields.Str(validate=validate.OneOf(["Pending", "Accepted", "Rejected"]))


# ─── Notification ─────────────────────────────────────────────────────────────

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True


# ─── Singleton instances used across routes ───────────────────────────────────

institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

challenge_schema = ChallengeSchema()
challenges_schema = ChallengeSchema(many=True)

weekly_schema = WeeklyChallengeSchema()

submission_schema = SubmissionSchema()
submissions_schema = SubmissionSchema(many=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

friend_schema = FriendRequestSchema()
friends_schema = FriendRequestSchema(many=True)

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
