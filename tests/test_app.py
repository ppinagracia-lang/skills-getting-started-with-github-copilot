import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


BASELINE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(BASELINE_ACTIVITIES))
    return TestClient(app_module.app)


def test_signup_for_activity_success(client):
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected(client):
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert activities_response.json()["Chess Club"]["participants"].count(email) == 1


def test_unregister_participant_removes_student(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/participants/{email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email not in activities_response.json()["Chess Club"]["participants"]
