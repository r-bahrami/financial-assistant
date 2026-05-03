#!/usr/bin/env python3
"""
Database Migration: Add User Authentication Support
Creates users and user_sessions tables for authentication
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def migrate():
    """Add users and user_sessions tables to database"""
    
    print("=" * 60)
    print("Migration: Adding User Authentication Support")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if tables already exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('users', 'user_sessions')
        """)
        existing = [row[0] for row in cursor.fetchall()]
        
        if existing:
            print(f"⚠️  Tables already exist: {', '.join(existing)}")
            print("   Skipping migration to avoid data loss")
            return
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Create users table
        print("\n1. Creating users table...")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                encryption_salt TEXT NOT NULL,
                encrypted_db_key TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        print("   ✅ users table created")
        
        # Create user_sessions table
        print("\n2. Creating user_sessions table...")
        cursor.execute("""
            CREATE TABLE user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("   ✅ user_sessions table created")
        
        # Create indexes for performance
        print("\n3. Creating indexes...")
        cursor.execute("CREATE INDEX idx_users_username ON users(username);")
        cursor.execute("CREATE INDEX idx_users_email ON users(email);")
        cursor.execute("CREATE INDEX idx_sessions_user ON user_sessions(user_id);")
        cursor.execute("CREATE INDEX idx_sessions_token ON user_sessions(session_token);")
        cursor.execute("CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);")
        print("   ✅ Indexes created")
        
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
