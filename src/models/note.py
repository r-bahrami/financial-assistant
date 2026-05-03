"""
Model helpers for transaction notes.
"""

import sqlite3
from typing import Dict, Optional, List

from .transaction import Transaction


class TransactionNote:
    """CRUD helpers for notes stored in transaction_notes table."""

    @staticmethod
    def _get_db_path() -> str:
        try:
            from flask import current_app

            return current_app.config.get("DATABASE", Transaction._get_db_path())
        except (ImportError, RuntimeError):
            return Transaction._get_db_path()

    @classmethod
    def get(cls, transaction_id: int) -> Optional[Dict]:
        """Fetch the note for a single transaction."""
        conn = sqlite3.connect(cls._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, transaction_id, note, created_at, updated_at
            FROM transaction_notes
            WHERE transaction_id = ?
            """,
            (transaction_id,),
        )
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    @classmethod
    def get_for_transactions(cls, transaction_ids: List[int]) -> Dict[int, Dict]:
        """Fetch notes for a list of transaction IDs."""
        if not transaction_ids:
            return {}

        conn = sqlite3.connect(cls._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        placeholders = ",".join("?" * len(transaction_ids))
        cursor.execute(
            f"""
            SELECT id, transaction_id, note, created_at, updated_at
            FROM transaction_notes
            WHERE transaction_id IN ({placeholders})
            """,
            transaction_ids,
        )

        results = {row["transaction_id"]: dict(row) for row in cursor.fetchall()}
        conn.close()
        return results

    @classmethod
    def upsert(cls, transaction_id: int, note_text: str) -> Dict:
        """Create or update the note for a transaction."""
        existing = cls.get(transaction_id)
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()

        if existing:
            cursor.execute(
                """
                UPDATE transaction_notes
                SET note = ?, updated_at = CURRENT_TIMESTAMP
                WHERE transaction_id = ?
                """,
                (note_text, transaction_id),
            )
        else:
            cursor.execute(
                """
                INSERT INTO transaction_notes (transaction_id, note, created_at, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """,
                (transaction_id, note_text),
            )

        conn.commit()
        conn.close()
        return cls.get(transaction_id)

    @classmethod
    def delete(cls, transaction_id: int) -> bool:
        """Delete the note for a transaction."""
        conn = sqlite3.connect(cls._get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transaction_notes WHERE transaction_id = ?", (transaction_id,)
        )
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

