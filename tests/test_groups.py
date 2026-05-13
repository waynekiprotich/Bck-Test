import pytest


def test_create_group_requires_auth(client):
    res = client.post("/groups/", json={"name": "Test Group"})
    assert res.status_code == 401


def test_create_group_success(client, auth_headers):
    res = client.post("/groups/", headers=auth_headers, json={
        "name": "Nairobi Coders",
        "description": "A group for Nairobi developers",
    })
    assert res.status_code == 201
    body = res.get_json()
    assert body["name"] == "Nairobi Coders"
    assert "invite_code" in body
    assert len(body["invite_code"]) == 8


def test_create_group_missing_name(client, auth_headers):
    res = client.post("/groups/", headers=auth_headers, json={
        "description": "No name provided",
    })
    assert res.status_code == 400


def test_list_groups(client, auth_headers):
    client.post("/groups/", headers=auth_headers, json={"name": "My Group"})
    res = client.get("/groups/", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_join_group_success(client, auth_headers):
    # Create group with user A
    create_res = client.post("/groups/", headers=auth_headers, json={
        "name": "Join Me Group",
    })
    invite_code = create_res.get_json()["invite_code"]

    # Register user B
    client.post("/auth/register", json={
        "name": "User B",
        "email": "userb@test.com",
        "password": "password123",
    })
    login_res = client.post("/auth/login", json={
        "email": "userb@test.com",
        "password": "password123",
    })
    headers_b = {"Authorization": f"Bearer {login_res.get_json()['token']}"}

    # User B joins with invite code
    res = client.post("/groups/join", headers=headers_b, json={
        "invite_code": invite_code,
    })
    assert res.status_code == 200


def test_join_group_already_member(client, auth_headers):
    create_res = client.post("/groups/", headers=auth_headers, json={
        "name": "Duplicate Join Group",
    })
    invite_code = create_res.get_json()["invite_code"]

    # Try to join own group (already a member as admin)
    res = client.post("/groups/join", headers=auth_headers, json={
        "invite_code": invite_code,
    })
    assert res.status_code == 409


def test_join_group_invalid_code(client, auth_headers):
    res = client.post("/groups/join", headers=auth_headers, json={
        "invite_code": "XXXXXXXX",
    })
    assert res.status_code == 404


def test_get_group_by_id(client, auth_headers):
    create_res = client.post("/groups/", headers=auth_headers, json={
        "name": "Get By ID Group",
    })
    group_id = create_res.get_json()["id"]
    res = client.get(f"/groups/{group_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["id"] == group_id
