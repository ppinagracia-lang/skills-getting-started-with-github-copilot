from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    email = "teststudent@mergington.edu"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activity = activities_response.json()["Chess Club"]
    assert email not in activity["participants"]
