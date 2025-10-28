from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "pytest_temp_user@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    try:
        # Sign up
        signup_res = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
        assert signup_res.status_code == 200
        assert email in activities[activity]["participants"]

        # Unregister
        del_res = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
        assert del_res.status_code == 200
        assert email not in activities[activity]["participants"]
    finally:
        # Cleanup just in case
        if email in activities[activity]["participants"]:
            activities[activity]["participants"].remove(email)
