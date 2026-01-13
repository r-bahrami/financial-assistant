#!/usr/bin/env python3
"""
Reset Admin User Password
Utility script to reset the password for an admin user
"""

import sqlite3
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))
from services.password_service import PasswordService

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def reset_admin_password(username: str, new_password: str):
    """Reset password for an admin user."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if user exists and is admin
        cursor.execute("""
            SELECT id, username, role FROM users WHERE username = ?
        """, (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User '{username}' not found")
            return False
        
        user_id, db_username, role = user
        
        if role != 'admin':
            print(f"⚠️  User '{username}' is not an admin (role: {role})")
            response = input("Do you want to reset their password anyway? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Password reset cancelled")
                return False
        
        # Validate password strength
        is_valid, error_msg = PasswordService.validate_password_strength(new_password)
        if not is_valid:
            print(f"❌ Password validation failed: {error_msg}")
            return False
        
        # Hash new password
        password_hash = PasswordService.hash_password(new_password)
        
        # Update password
        cursor.execute("""
            UPDATE users 
            SET password_hash = ? 
            WHERE id = ?
        """, (password_hash, user_id))
        
        conn.commit()
        print(f"✅ Password reset successfully for user '{username}'")
        print(f"   User ID: {user_id}")
        print(f"   Role: {role}")
        return True
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"❌ Database error: {e}")
        return False
    finally:
        conn.close()

def list_admin_users():
    """List all admin users."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, username, email, role, created_at 
            FROM users 
            WHERE role = 'admin'
            ORDER BY id
        """)
        admins = cursor.fetchall()
        
        if not admins:
            print("⚠️  No admin users found")
            return
        
        print("\nAdmin users:")
        print("-" * 60)
        for user_id, username, email, role, created_at in admins:
            print(f"  ID {user_id}: {username} ({email})")
            print(f"    Created: {created_at}")
            print()
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def main():
    """Main function."""
    
    print("=" * 60)
    print("Admin Password Reset Utility")
    print("=" * 60)
    
    # List admin users
    list_admin_users()
    
    # Get username
    username = input("\nEnter admin username to reset password: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return
    
    # Get new password
    new_password = input("Enter new password: ").strip()
    if not new_password:
        print("❌ Password cannot be empty")
        return
    
    # Confirm password
    confirm_password = input("Confirm new password: ").strip()
    if new_password != confirm_password:
        print("❌ Passwords do not match")
        return
    
    # Reset password
    print()
    success = reset_admin_password(username, new_password)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Password reset complete!")
        print("=" * 60)
        print(f"\nYou can now log in with:")
        print(f"  Username: {username}")
        print(f"  Password: {new_password}")
    else:
        print("\n" + "=" * 60)
        print("❌ Password reset failed")
        print("=" * 60)

if __name__ == '__main__':
    main()
