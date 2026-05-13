import pytest
from app.models.challenge import Challenge, TestCase


def _make_challenge(db, title="Test Challenge", difficulty="Easy", is_practice=True):
    """Helper to create and persist a challenge."""
    c = Challenge(
        title=title,
        slug=title.lower().replace(" ", "-"),
        description="A test challenge.",
        difficulty=difficulty,
        points_reward=50 if difficulty == "Easy" else 100,
        is_practice=is_practice,
    )
    db.session.add(c)
    db.session.commit()
    return c


def test_get_challenges_requires_auth(client):
    res = client.get("/challenges/")
    assert res.status_code == 401


def test_get_challenges_returns_paginated(client, auth_headers, db):
    for i in range(5):
        _make_challenge(db, title=f"Challenge {i}")

    res = client.get("/challenges/?page=1&per_page=3", headers=auth_headers)
    assert res.status_code == 200
    body = res.get_json()
    assert "data" in body
    assert "pagination" in body
    assert len(body["data"]) <= 3


def test_get_challenges_filter_by_difficulty(client, auth_headers, db):
    _make_challenge(db, title="Easy One",   difficulty="Easy")
    _make_challenge(db, title="Hard One",   difficulty="Hard")

    res = client.get("/challenges/?difficulty=Hard", headers=auth_headers)
    assert res.status_code == 200
    for ch in res.get_json()["data"]:
        assert ch["difficulty"] == "Hard"


def test_get_challenges_invalid_difficulty(client, auth_headers):
    res = client.get("/challenges/?difficulty=Impossible", headers=auth_headers)
    assert res.status_code == 400


def test_get_challenge_by_id(client, auth_headers, db):
    c = _make_challenge(db, title="Unique Challenge XYZ")
    res = client.get(f"/challenges/{c.id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["title"] == "Unique Challenge XYZ"


def test_get_challenge_not_found(client, auth_headers):
    res = client.get("/challenges/999999", headers=auth_headers)
    assert res.status_code == 404


def test_get_practice_challenges(client, auth_headers, db):
    _make_challenge(db, title="Practice A", is_practice=True)
    _make_challenge(db, title="Competition B", is_practice=False)

    res = client.get("/challenges/practice", headers=auth_headers)
    assert res.status_code == 200
    for ch in res.get_json()["data"]:
        assert ch["is_practice"] is True
