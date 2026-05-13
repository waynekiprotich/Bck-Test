import pytest


def test_check_email_not_exists(client):
    res = client.post("/auth/check-email", json={"email": "nobody@test.com"})
    assert res.status_code == 200
    assert res.get_json()["exists"] is False


def test_check_email_missing(client):
    res = client.post("/auth/check-email", json={})
    assert res.status_code == 400


def test_register_success(client):
    res = client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice_reg@test.com",
        "password": "strongpass1",
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "token" in data
    assert data["user"]["email"] == "alice_reg@test.com"
    assert "password_hash" not in data["user"]  # must never be exposed


def test_register_duplicate_email(client):
    payload = {"name": "Bob", "email": "dup@test.com", "password": "pass1234"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code in [409, 422]


def test_register_short_password(client):
    res = client.post("/auth/register", json={
        "name": "Charlie",
        "email": "charlie@test.com",
        "password": "short",
    })
    assert res.status_code == 422


def test_register_invalid_email(client):
    res = client.post("/auth/register", json={
        "name": "Dan",
        "email": "not-an-email",
        "password": "password123",
    })
    assert res.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json={
        "name": "Eve",
        "email": "eve@test.com",
        "password": "mypassword1",
    })
    res = client.post("/auth/login", json={
        "email": "eve@test.com",
        "password": "mypassword1",
    })
    assert res.status_code == 200
    assert "token" in res.get_json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "Frank",
        "email": "frank@test.com",
        "password": "correctpass1",
    })
    res = client.post("/auth/login", json={
        "email": "frank@test.com",
        "password": "wrongpass",
    })
    assert res.status_code == 401


def test_me_requires_auth(client):
    res = client.get("/auth/me")
    assert res.status_code == 401


def test_me_with_valid_token(client, auth_headers):
    res = client.get("/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert "email" in res.get_json()
