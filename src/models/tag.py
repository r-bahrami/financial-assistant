"""Tag model helpers."""

import sqlite3
from typing import Dict, List, Optional

from .transaction import Transaction


class Tag:
    """CRUD helpers for tags and transaction tag relationships."""

    @staticmethod
    def _get_db_path() -> str:
        try:
            from flask import current_app

            return current_app.config.get("DATABASE", Transaction._get_db_path())
        except (ImportError, RuntimeError):
            return Transaction._get_db_path()

    @classmethod
    def get_all(cls) -> List[Dict]:
        conn = sqlite3.connect(cls._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, color, created_at
            FROM tags
            ORDER BY name COLLATE NOCASE
            """
        )
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @classmethod
    def create(cls, name: str, color: str) -> Dict:
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tags (name, color, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            """,
            (name.strip(), color),
        )
        conn.commit()
        tag_id = cursor.lastrowid
        conn.close()
        return cls.get(tag_id)

    @classmethod
    def get(cls, tag_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(cls._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, color, created_at FROM tags WHERE id = ?", (tag_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @classmethod
    def update(cls, tag_id: int, name: str, color: str) -> Optional[Dict]:
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE tags
            SET name = ?, color = ?
            WHERE id = ?
            """,
            (name.strip(), color, tag_id),
        )
        conn.commit()
        conn.close()
        return cls.get(tag_id)

    @classmethod
    def delete(cls, tag_id: int) -> bool:
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        deleted = cursor.rowcount > 0
        if deleted:
            cursor.execute("DELETE FROM transaction_tags WHERE tag_id = ?", (tag_id,))
        conn.commit()
        conn.close()
        return deleted

    @classmethod
    def get_for_transaction(cls, transaction_id: int) -> List[Dict]:
        conn = sqlite3.connect(cls._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.id, t.name, t.color
            FROM tags t
            JOIN transaction_tags tt ON tt.tag_id = t.id
            WHERE tt.transaction_id = ?
            ORDER BY t.name COLLATE NOCASE
            """,
            (transaction_id,),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @classmethod
    def get_for_transactions(cls, transaction_ids: List[int]) -> Dict[int, List[Dict]]:
        if not transaction_ids:
            return {}

        conn = sqlite3.connect(cls._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        placeholders = ",".join("?" * len(transaction_ids))
        cursor.execute(
            f"""
            SELECT tt.transaction_id, t.id, t.name, t.color
            FROM transaction_tags tt
            JOIN tags t ON t.id = tt.tag_id
            WHERE tt.transaction_id IN ({placeholders})
            ORDER BY t.name COLLATE NOCASE
            """,
            transaction_ids,
        )

        mapping: Dict[int, List[Dict]] = {}
        for row in cursor.fetchall():
            txn_id = row["transaction_id"]
            mapping.setdefault(txn_id, []).append(
                {"id": row["id"], "name": row["name"], "color": row["color"]}
            )
        conn.close()
        return mapping

    @classmethod
    def set_for_transaction(cls, transaction_id: int, tag_ids: List[int]) -> List[Dict]:
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM transaction_tags WHERE transaction_id = ?", (transaction_id,)
        )
        if tag_ids:
            cursor.executemany(
                """
                INSERT INTO transaction_tags (transaction_id, tag_id, created_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                """,
                [(transaction_id, tag_id) for tag_id in tag_ids],
            )
        conn.commit()
        conn.close()
        return cls.get_for_transaction(transaction_id)

    @classmethod
    def bulk_set(cls, transaction_ids: List[int], tag_ids: List[int]) -> int:
        """Replace tags for many transactions at once."""
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()

        placeholders = ",".join("?" * len(transaction_ids))
        cursor.execute(
            f"DELETE FROM transaction_tags WHERE transaction_id IN ({placeholders})",
            transaction_ids,
        )
        if tag_ids:
            cursor.executemany(
                """
                INSERT INTO transaction_tags (transaction_id, tag_id, created_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                """,
                [(txn_id, tag_id) for txn_id in transaction_ids for tag_id in tag_ids],
            )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected

