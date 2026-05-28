def test_get_activities_returns_200(client):
    response = client.get("/activities")

    assert response.status_code == 200


def test_get_activities_response_shape(client):
    response = client.get("/activities")
    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_get_activities_includes_expected_fields(client):
    response = client.get("/activities")
    data = response.json()

    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity