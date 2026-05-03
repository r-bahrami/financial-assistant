"""
Goals Blueprint
Handles CRUD operations and UI for savings goals.
"""

from datetime import date, datetime
from typing import Dict, Tuple, Any, List

from flask import Blueprint, jsonify, request, current_app, render_template

from models.goal import Goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

GOAL_STATUSES = {"active", "completed", "cancelled"}
DEFAULT_GOAL_STATUS = "active"


@goals_bp.route("/")
def goals_page():
    """Render the savings goals management page."""
    return render_template("goals.html")


@goals_bp.route("/api", methods=["GET"])
def list_goals():
    """Return all savings goals with summary metrics."""
    goal_model = Goal(current_app.config["DATABASE"])
    goals = [_serialize_goal(goal) for goal in goal_model.get_all()]
    summary = _build_summary(goals)
    return jsonify({"success": True, "goals": goals, "summary": summary})


@goals_bp.route("/api/<int:goal_id>", methods=["GET"])
def get_goal(goal_id: int):
    """Return a single savings goal."""
    goal_model = Goal(current_app.config["DATABASE"])
    goal = goal_model.get_by_id(goal_id)
    if not goal:
        return jsonify({"success": False, "error": "Goal not found"}), 404
    return jsonify({"success": True, "goal": _serialize_goal(goal)})


@goals_bp.route("/api", methods=["POST"])
def create_goal():
    """Create a new savings goal."""
    data = request.get_json(silent=True) or {}
    payload, errors = _validate_goal_payload(data, is_update=False)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    goal_model = Goal(current_app.config["DATABASE"])
    goal_id = goal_model.create(
        name=payload["name"],
        target_amount=payload["target_amount"],
        current_amount=payload["current_amount"],
        target_date=payload["target_date"],
        category_id=payload["category_id"],
        status=payload["status"],
    )
    created_goal = goal_model.get_by_id(goal_id)
    return (
        jsonify({"success": True, "goal": _serialize_goal(created_goal)}),
        201,
    )


@goals_bp.route("/api/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id: int):
    """Update an existing savings goal."""
    data = request.get_json(silent=True) or {}
    payload, errors = _validate_goal_payload(data, is_update=True)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    goal_model = Goal(current_app.config["DATABASE"])
    existing_goal = goal_model.get_by_id(goal_id)
    if not existing_goal:
        return jsonify({"success": False, "error": "Goal not found"}), 404

    if payload:
        goal_model.update(goal_id, payload)

    updated_goal = goal_model.get_by_id(goal_id)
    return jsonify({"success": True, "goal": _serialize_goal(updated_goal)})


@goals_bp.route("/api/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id: int):
    """Delete a savings goal."""
    goal_model = Goal(current_app.config["DATABASE"])
    existing_goal = goal_model.get_by_id(goal_id)
    if not existing_goal:
        return jsonify({"success": False, "error": "Goal not found"}), 404

    success = goal_model.delete(goal_id)
    if not success:
        return jsonify({"success": False, "error": "Unable to delete goal"}), 500

    return jsonify({"success": True})


def _validate_goal_payload(data: Dict[str, Any], *, is_update: bool) -> Tuple[Dict[str, Any], List[str]]:
    """Validate and normalize goal payload."""
    errors: List[str] = []
    normalized: Dict[str, Any] = {}

    if not is_update or "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            errors.append("Goal name is required.")
        else:
            normalized["name"] = name

    if not is_update or "target_amount" in data:
        if "target_amount" not in data:
            errors.append("Target amount is required.")
        else:
            try:
                target_amount = float(data.get("target_amount", 0))
                if target_amount <= 0:
                    raise ValueError
                normalized["target_amount"] = target_amount
            except (TypeError, ValueError):
                errors.append("Target amount must be a positive number.")

    if not is_update or "current_amount" in data:
        current_amount_raw = data.get("current_amount", 0 if not is_update else None)
        if current_amount_raw is not None:
            try:
                current_amount = float(current_amount_raw)
                if current_amount < 0:
                    raise ValueError
                normalized["current_amount"] = current_amount
            except (TypeError, ValueError):
                errors.append("Current amount must be zero or a positive number.")

    if not is_update or "target_date" in data:
        target_date = data.get("target_date")
        if target_date:
            try:
                datetime.strptime(target_date, "%Y-%m-%d")
                normalized["target_date"] = target_date
            except (TypeError, ValueError):
                errors.append("Target date must be in YYYY-MM-DD format.")
        elif not is_update:
            normalized["target_date"] = None
        elif "target_date" in data:
            normalized["target_date"] = None

    if not is_update or "category_id" in data:
        category_raw = data.get("category_id")
        if category_raw in (None, "", "null"):
            normalized["category_id"] = None
        else:
            try:
                category_id = int(category_raw)
                if category_id <= 0:
                    raise ValueError
                normalized["category_id"] = category_id
            except (TypeError, ValueError):
                errors.append("Category must be a positive integer or null.")

    if not is_update or "status" in data:
        status = (data.get("status") or DEFAULT_GOAL_STATUS).lower()
        if status not in GOAL_STATUSES:
            errors.append("Status must be active, completed, or cancelled.")
        else:
            normalized["status"] = status

    # Ensure defaults for creation
    if not is_update:
        normalized.setdefault("current_amount", 0.0)
        normalized.setdefault("status", DEFAULT_GOAL_STATUS)

    return normalized, errors


def _serialize_goal(goal: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize database row into API-friendly goal representation."""
    target_amount = float(goal.get("target_amount") or 0.0)
    current_amount = float(goal.get("current_amount") or 0.0)
    status = goal.get("status") or DEFAULT_GOAL_STATUS

    progress_percentage = 0.0
    if target_amount > 0:
        progress_percentage = max(0.0, min(100.0, (current_amount / target_amount) * 100))

    remaining_amount = max(0.0, target_amount - current_amount)

    target_date = goal.get("target_date")
    days_remaining = None
    is_overdue = False
    if target_date:
        try:
            due_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            days_remaining = (due_date - date.today()).days
            is_overdue = status != "completed" and days_remaining < 0
        except ValueError:
            target_date = None

    return {
        "id": goal.get("id"),
        "name": goal.get("name"),
        "target_amount": round(target_amount, 2),
        "current_amount": round(current_amount, 2),
        "remaining_amount": round(remaining_amount, 2),
        "progress_percentage": round(progress_percentage, 2),
        "status": status,
        "target_date": target_date,
        "category_id": goal.get("category_id"),
        "category_name": goal.get("category_name"),
        "days_remaining": days_remaining,
        "is_overdue": is_overdue,
        "created_at": goal.get("created_at"),
        "updated_at": goal.get("updated_at"),
    }


def _build_summary(goals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate summary metrics for goals collection."""
    if not goals:
        return {
            "total_target": 0.0,
            "total_saved": 0.0,
            "average_progress": 0.0,
            "active_count": 0,
            "completed_count": 0,
        }

    total_target = sum(goal["target_amount"] for goal in goals)
    total_saved = sum(goal["current_amount"] for goal in goals)
    average_progress = sum(goal["progress_percentage"] for goal in goals) / len(goals)
    active_count = sum(1 for goal in goals if goal["status"] == "active")
    completed_count = sum(1 for goal in goals if goal["status"] == "completed")

    return {
        "total_target": round(total_target, 2),
        "total_saved": round(total_saved, 2),
        "average_progress": round(average_progress, 2),
        "active_count": active_count,
        "completed_count": completed_count,
    }

