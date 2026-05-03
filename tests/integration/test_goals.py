from datetime import date, timedelta

import pytest


def test_goals_crud_flow(client, sample_category):
    """End-to-end test covering goal creation, update, listing, and deletion."""
    # Initial state
    response = client.get("/goals/api")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["goals"] == []

    target_date = (date.today() + timedelta(days=180)).isoformat()
    create_payload = {
        "name": "Emergency Fund",
        "target_amount": 5000,
        "current_amount": 500,
        "target_date": target_date,
        "category_id": sample_category,
        "status": "active",
    }

    create_response = client.post("/goals/api", json=create_payload)
    assert create_response.status_code == 201
    created = create_response.get_json()
    assert created["success"] is True
    goal = created["goal"]
    assert goal["name"] == "Emergency Fund"
    assert goal["target_amount"] == pytest.approx(5000.0, rel=1e-3)
    assert goal["current_amount"] == pytest.approx(500.0, rel=1e-3)
    assert goal["category_id"] == sample_category
    goal_id = goal["id"]

    # Ensure list endpoint reflects newly created goal and summary
    list_response = client.get("/goals/api")
    data = list_response.get_json()
    assert len(data["goals"]) == 1
    assert data["summary"]["total_target"] == pytest.approx(5000.0, rel=1e-3)
    assert data["summary"]["total_saved"] == pytest.approx(500.0, rel=1e-3)

    # Update goal progress and status
    update_response = client.put(
        f"/goals/api/{goal_id}",
        json={"current_amount": 5000, "status": "completed"},
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()
    assert updated["success"] is True
    assert updated["goal"]["status"] == "completed"
    assert updated["goal"]["progress_percentage"] == pytest.approx(100.0, rel=1e-3)

    # Delete the goal
    delete_response = client.delete(f"/goals/api/{goal_id}")
    assert delete_response.status_code == 200
    delete_payload = delete_response.get_json()
    assert delete_payload["success"] is True

    final_list = client.get("/goals/api").get_json()
    assert final_list["goals"] == []
    assert final_list["summary"]["total_target"] == 0.0


def test_goal_validation_errors(client):
    """Ensure validation catches invalid payloads."""
    invalid_response = client.post(
        "/goals/api",
        json={"name": "", "target_amount": -100},
    )
    assert invalid_response.status_code == 400
    errors = invalid_response.get_json()["errors"]
    assert "Goal name is required." in errors
    assert "Target amount must be a positive number." in errors

    missing_goal = client.put("/goals/api/9999", json={"name": "Updated"})
    assert missing_goal.status_code == 404
    assert missing_goal.get_json()["success"] is False

