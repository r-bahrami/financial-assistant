"""Tag management routes."""

from flask import Blueprint, jsonify, request
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.tag import Tag

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")


@tags_bp.route("/api", methods=["GET"])
def list_tags():
    try:
        return jsonify({"success": True, "tags": Tag.get_all()})
    except Exception as exc:  # pragma: no cover - safety net
        return jsonify({"success": False, "error": str(exc)}), 500


@tags_bp.route("/api", methods=["POST"])
def create_tag():
    try:
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        color = data.get("color") or "#667eea"

        if not name:
            return jsonify({"success": False, "error": "Tag name is required"}), 400

        tag = Tag.create(name, color)
        return jsonify({"success": True, "tag": tag})
    except Exception as exc:  # pragma: no cover
        return jsonify({"success": False, "error": str(exc)}), 500


@tags_bp.route("/api/<int:tag_id>", methods=["PUT"])
def update_tag(tag_id: int):
    try:
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        color = data.get("color") or "#667eea"

        if not name:
            return jsonify({"success": False, "error": "Tag name is required"}), 400

        updated = Tag.update(tag_id, name, color)
        if not updated:
            return jsonify({"success": False, "error": "Tag not found"}), 404

        return jsonify({"success": True, "tag": updated})
    except Exception as exc:  # pragma: no cover
        return jsonify({"success": False, "error": str(exc)}), 500


@tags_bp.route("/api/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id: int):
    try:
        if not Tag.delete(tag_id):
            return jsonify({"success": False, "error": "Tag not found"}), 404
        return jsonify({"success": True})
    except Exception as exc:  # pragma: no cover
        return jsonify({"success": False, "error": str(exc)}), 500


@tags_bp.route("/api/transaction/<int:transaction_id>", methods=["GET", "PUT"])
def transaction_tags(transaction_id: int):
    try:
        if request.method == "GET":
            return jsonify({"success": True, "tags": Tag.get_for_transaction(transaction_id)})

        payload = request.get_json() or {}
        tag_ids = payload.get("tag_ids", [])
        updated = Tag.set_for_transaction(transaction_id, tag_ids)
        return jsonify({"success": True, "tags": updated})
    except Exception as exc:  # pragma: no cover
        return jsonify({"success": False, "error": str(exc)}), 500


@tags_bp.route("/api/bulk", methods=["POST"])
def bulk_tag():
    try:
        payload = request.get_json() or {}
        transaction_ids = payload.get("transaction_ids") or []
        tag_ids = payload.get("tag_ids") or []

        if not transaction_ids:
            return jsonify({"success": False, "error": "No transaction IDs provided"}), 400

        Tag.bulk_set(transaction_ids, tag_ids)
        return jsonify({"success": True})
    except Exception as exc:  # pragma: no cover
        return jsonify({"success": False, "error": str(exc)}), 500

