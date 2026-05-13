import pytest


def _register_and_login(client, name, email):
    client.post("/auth/register", json={
        "name": name,
        "email": email,
        "password": "password123",
    })
    res = client.post("/auth/login", json={
        "email": email,
        "password": "password123",
    })
    data = res.get_json()
    token = data["token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_send_friend_request_success(client):
    headers_a, id_a = _register_and_login(client, "Alpha", "alpha@t.com")
    headers_b, id_b = _register_and_login(client, "Beta",  "beta@t.com")

    res = client.post("/friends/request", headers=headers_a, json={
        "receiver_id": id_b,
    })
    assert res.status_code == 201
    assert "id" in res.get_json()


def test_send_self_request(client, auth_headers):
    # Get own user ID
    me = client.get("/auth/me", headers=auth_headers).get_json()
    res = client.post("/friends/request", headers=auth_headers, json={
        "receiver_id": me["id"],
    })
    assert res.status_code == 400


def test_duplicate_friend_request(client):
    headers_a, id_a = _register_and_login(client, "Gamma", "gamma@t.com")
    headers_b, id_b = _register_and_login(client, "Delta", "delta@t.com")

    client.post("/friends/request", headers=headers_a, json={"receiver_id": id_b})
    res = client.post("/friends/request", headers=headers_a, json={"receiver_id": id_b})
    assert res.status_code == 400


def test_accept_friend_request(client):
    headers_a, id_a = _register_and_login(client, "Epsilon", "eps@t.com")
    headers_b, id_b = _register_and_login(client, "Zeta",    "zeta@t.com")

    req_res = client.post("/friends/request", headers=headers_a, json={"receiver_id": id_b})
    req_id  = req_res.get_json()["id"]

    res = client.put(f"/friends/{req_id}/status", headers=headers_b, json={
        "status": "Accepted",
    })
    assert res.status_code == 200


def test_reject_friend_request(client):
    headers_a, id_a = _register_and_login(client, "Eta",   "eta@t.com")
    headers_b, id_b = _register_and_login(client, "Theta", "theta@t.com")

    req_res = client.post("/friends/request", headers=headers_a, json={"receiver_id": id_b})
    req_id  = req_res.get_json()["id"]

    res = client.put(f"/friends/{req_id}/status", headers=headers_b, json={
        "status": "Rejected",
    })
    assert res.status_code == 200


def test_only_receiver_can_accept(client):
    headers_a, id_a = _register_and_login(client, "Iota",  "iota@t.com")
    headers_b, id_b = _register_and_login(client, "Kappa", "kappa@t.com")

    req_res = client.post("/friends/request", headers=headers_a, json={"receiver_id": id_b})
    req_id  = req_res.get_json()["id"]

    # Sender tries to accept their own request — should be forbidden
    res = client.put(f"/friends/{req_id}/status", headers=headers_a, json={
        "status": "Accepted",
    })
    assert res.status_code == 403


def test_list_friends_requires_auth(client):
    res = client.get("/friends/")
    assert res.status_code == 401


def test_list_friends(client, auth_headers):
    res = client.get("/friends/", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
