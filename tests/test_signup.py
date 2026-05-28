from urllib.parse import quote


def signup_path(activity_name):
    return f"/activities/{quote(activity_name, safe='')}/signup"


def unregister_path(activity_name):
    return f"/activities/{quote(activity_name, safe='')}/participants"


def test_signup_new_student_returns_200(client):
    email = "newstudent@mergington.edu"
    response = client.post(signup_path("Chess Club"), params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_adds_email_to_participants_list(client):
    email = "participantcheck@mergington.edu"
    response = client.post(signup_path("Programming Class"), params={"email": email})

    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities["Programming Class"]["participants"]


def test_signup_duplicate_email_returns_400(client):
    email = "duplicate@mergington.edu"

    first_signup = client.post(signup_path("Gym Class"), params={"email": email})
    second_signup = client.post(signup_path("Gym Class"), params={"email": email})

    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert second_signup.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    response = client.post(signup_path("Nonexistent Club"), params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_then_unregister_lifecycle(client):
    email = "lifecycle@mergington.edu"

    signup_response = client.post(signup_path("Debate Team"), params={"email": email})
    unregister_response = client.delete(unregister_path("Debate Team"), params={"email": email})

    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Debate Team"]["participants"]