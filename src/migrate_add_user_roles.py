#!/usr/bin/env python3
"""
Database Migration: Add User Roles
Adds role column to users table for admin/user distinction
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def migrate():
    """Add role column to users table"""
    
    print("=" * 60)
    print("Migration: Adding User Roles")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if role column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'role' in columns:
            print("⚠️  role column already exists")
            print("   Skipping migration to avoid data loss")
            conn.close()
            return
        
        # Add role column
        print("\n1. Adding role column to users table...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user'))
        """)
        print("   ✅ role column added")
        
        # Make first user (if exists) an admin
        cursor.execute("SELECT id, username FROM users ORDER BY id LIMIT 1")
        first_user = cursor.fetchone()
        
        if first_user:
            user_id, username = first_user
            cursor.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
            print(f"   ✅ First user '{username}' (ID: {user_id}) set as admin")
        else:
            print("   ℹ️  No users found - first registered user will be admin")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
