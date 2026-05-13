from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.extensions import db
from app.models.user import User
from app.schemas import user_schema


def check_email_exists(email: str) -> bool:
    return User.query.filter_by(email=email.lower().strip()).first() is not None


def register_user(data: dict) -> dict:
    """
    Validate input, create a new User, and return a JWT + user object.
    Raises ValidationError if input is invalid.
    Raises ValueError if email is already registered.
    """
    # Validate with schema 
    errors = user_schema.validate(data)
    if errors:
        raise ValidationError(errors)

    email = data.get("email", "").lower().strip()

    # Guard duplicate email
    if check_email_exists(email):
        raise ValueError("An account with this email already exists.")

    # Build user — never store the raw password
    user = User(
        name=data["name"].strip(),
        email=email,
        institution_id=data.get("institution_id"),
        bio=data.get("bio", ""),
        avatar_url=data.get("avatar_url", ""),
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return {"token": token, "user": user_schema.dump(user)}


def login_user(data: dict) -> dict:
    """
    Verify email + password and return a JWT + user object.
    Raises ValueError on invalid credentials.
    """
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        raise ValueError("Invalid email or password.")

    token = create_access_token(identity=user.id)
    return {"token": token, "user": user_schema.dump(user)}
