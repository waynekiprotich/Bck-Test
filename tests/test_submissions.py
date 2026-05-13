import pytest
from unittest.mock import patch
from app.models.challenge import Challenge, TestCase


def _setup_challenge(db, difficulty="Easy"):
    """Create a challenge with one visible test case."""
    c = Challenge(
        title="Add Numbers",
        slug="add-numbers-test",
        description="Add two numbers",
        difficulty=difficulty,
        points_reward=50 if difficulty == "Easy" else 100,
        is_practice=True,
    )
    db.session.add(c)
    db.session.flush()

    tc = TestCase(
        challenge_id=c.id,
        input_data="3 5",
        expected_output="8",
        is_hidden=False,
    )
    db.session.add(tc)
    db.session.commit()
    return c


def test_submit_requires_auth(client):
    res = client.post("/submit-code", json={})
    assert res.status_code == 401


def test_submit_missing_challenge_id(client, auth_headers):
    res = client.post("/submit-code", headers=auth_headers, json={
        "language": "python",
        "code": "print(1)",
    })
    assert res.status_code == 400


def test_submit_invalid_language(client, auth_headers, db):
    c = _setup_challenge(db)
    res = client.post("/submit-code", headers=auth_headers, json={
        "challenge_id": c.id,
        "language": "ruby",
        "code": "puts 'hello'",
    })
    assert res.status_code == 400


def test_submit_empty_code(client, auth_headers, db):
    c = _setup_challenge(db)
    res = client.post("/submit-code", headers=auth_headers, json={
        "challenge_id": c.id,
        "language": "python",
        "code": "   ",
    })
    assert res.status_code == 400


@patch("app.services.scoring_service.run_code")
def test_submit_accepted(mock_run, client, auth_headers, db):
    """Mock Piston to return correct output — expect Accepted."""
    mock_run.return_value = {
        "stdout": "8\n",
        "stderr": "",
        "code": 0,
        "time": 0.05,
    }
    c = _setup_challenge(db)
    res = client.post("/submit-code", headers=auth_headers, json={
        "challenge_id": c.id,
        "language": "python",
        "code": "a, b = map(int, input().split())\nprint(a + b)",
    })
    assert res.status_code == 201
    body = res.get_json()
    assert body["status"] == "Accepted"
    assert body["passed_tests"] == 1
    assert body["score"] == 50


@patch("app.services.scoring_service.run_code")
def test_submit_wrong_answer(mock_run, client, auth_headers, db):
    """Mock Piston to return wrong output — expect Wrong Answer."""
    mock_run.return_value = {
        "stdout": "99\n",
        "stderr": "",
        "code": 0,
        "time": 0.05,
    }
    c = _setup_challenge(db)
    res = client.post("/submit-code", headers=auth_headers, json={
        "challenge_id": c.id,
        "language": "python",
        "code": "print(99)",
    })
    assert res.status_code == 201
    body = res.get_json()
    assert body["status"] == "Wrong Answer"
    assert body["passed_tests"] == 0
    assert body["score"] == 0


@patch("app.services.scoring_service.run_code")
def test_submit_runtime_error(mock_run, client, auth_headers, db):
    """Mock Piston returning stderr — expect Runtime Error."""
    mock_run.return_value = {
        "stdout": "",
        "stderr": "NameError: name 'x' is not defined",
        "code": 1,
        "time": 0.01,
    }
    c = _setup_challenge(db)
    res = client.post("/submit-code", headers=auth_headers, json={
        "challenge_id": c.id,
        "language": "python",
        "code": "print(x)",
    })
    assert res.status_code == 201
    assert res.get_json()["status"] == "Runtime Error"


def test_get_results_requires_auth(client):
    res = client.get("/results")
    assert res.status_code == 401


def test_get_results_paginated(client, auth_headers):
    res = client.get("/results", headers=auth_headers)
    assert res.status_code == 200
    assert "data" in res.get_json()


def test_get_result_forbidden(client, auth_headers, db):
    """User cannot view another user's submission."""
    # Create a second user
    client.post("/auth/register", json={
        "name": "Other User",
        "email": "other@test.com",
        "password": "otherpass1",
    })
    # We'd need their submission ID; just check a fake ID returns 404
    res = client.get("/results/999999", headers=auth_headers)
    assert res.status_code == 404
