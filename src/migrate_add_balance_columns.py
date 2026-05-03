#!/usr/bin/env python3
"""
Migration script to add initial_balance and current_balance columns to accounts table.
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "financial_assistant.db"
)


def migrate():
    """Add initial_balance and current_balance columns to accounts table."""

    print("=" * 60)
    print("Migration: Add Balance Columns to Accounts")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check existing columns
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [row[1] for row in cursor.fetchall()]

        # Add initial_balance column if it doesn't exist
        if "initial_balance" not in columns:
            print("\n1. Adding initial_balance column...")
            cursor.execute("""
                ALTER TABLE accounts
                ADD COLUMN initial_balance DECIMAL(12, 2) DEFAULT 0.00
            """)
            print("   ✅ initial_balance column added")
        else:
            print("⚠️  initial_balance column already exists")

        # Add current_balance column if it doesn't exist
        if "current_balance" not in columns:
            print("\n2. Adding current_balance column...")
            cursor.execute("""
                ALTER TABLE accounts
                ADD COLUMN current_balance DECIMAL(12, 2) DEFAULT 0.00
            """)
            print("   ✅ current_balance column added")
        else:
            print("⚠️  current_balance column already exists")

        # Set initial_balance = current_balance for existing accounts
        print("\n3. Setting initial_balance = current_balance for existing accounts...")
        cursor.execute("""
            UPDATE accounts
            SET initial_balance = current_balance
            WHERE initial_balance = 0.00 OR initial_balance IS NULL
        """)
        print("   ✅ initial_balance set for existing accounts")

        conn.commit()
        print("\n✓ Migration completed successfully")

        # Show updated accounts
        cursor.execute(
            "SELECT id, name, initial_balance, current_balance FROM accounts"
        )
        accounts = cursor.fetchall()
        print(f"\nUpdated {len(accounts)} accounts:")
        for acc in accounts:
            print(
                f"  ID {acc[0]}: {acc[1]} - Initial: ${acc[2]:.2f}, Current: ${acc[3]:.2f}"
            )

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
