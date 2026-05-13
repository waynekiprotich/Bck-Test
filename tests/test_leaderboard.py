import pytest


def test_global_leaderboard_requires_auth(client):
    res = client.get("/leaderboard/")
    assert res.status_code == 401


def test_global_leaderboard_returns_data(client, auth_headers):
    res = client.get("/leaderboard/", headers=auth_headers)
    assert res.status_code == 200
    body = res.get_json()
    assert "data" in body
    assert "pagination" in body


def test_global_leaderboard_ordered_by_points(client, auth_headers):
    res = client.get("/leaderboard/?per_page=100", headers=auth_headers)
    data = res.get_json()["data"]
    points = [u["points"] for u in data]
    assert points == sorted(points, reverse=True)


def test_groups_leaderboard_requires_auth(client):
    res = client.get("/leaderboard/groups")
    assert res.status_code == 401


def test_groups_leaderboard_returns_data(client, auth_headers):
    # Create a group so the leaderboard has something
    client.post("/groups/", headers=auth_headers, json={"name": "LB Test Group"})
    res = client.get("/leaderboard/groups", headers=auth_headers)
    assert res.status_code == 200
    body = res.get_json()
    assert "data" in body
