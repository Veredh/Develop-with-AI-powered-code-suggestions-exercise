from urllib.parse import quote


def unregister_path(activity_name):
    return f"/activities/{quote(activity_name, safe='')}/participants"


def test_unregister_existing_participant_returns_200(client):
    response = client.delete(unregister_path("Chess Club"), params={"email": "michael@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"


def test_unregister_removes_email_from_participants_list(client):
    email = "sophia@mergington.edu"
    response = client.delete(unregister_path("Programming Class"), params={"email": email})

    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_not_signed_up_returns_404(client):
    response = client.delete(unregister_path("Tennis Club"), params={"email": "notenrolled@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_nonexistent_activity_returns_404(client):
    response = client.delete(unregister_path("Missing Club"), params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"