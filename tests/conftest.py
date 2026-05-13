import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Create a test app using an in-memory SQLite database."""
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    """Provide a DB session that rolls back after each test."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture
def auth_headers(client):
    """Register a test user, log in, and return JWT auth headers."""
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "password123",
    })
    res = client.post("/auth/login", json={
        "email": "testuser@test.com",
        "password": "password123",
    })
    token = res.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
