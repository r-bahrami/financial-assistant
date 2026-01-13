"""
User Model
Handles user authentication and user data management
"""

import sqlite3
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
import secrets
import sys
import os

# Add services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from services.password_service import PasswordService


class User:
    """Model for managing users."""
    
    def __init__(self, db_path: str):
        """
        Initialize User model.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def create(self, username: str, email: str, password_hash: str, 
               encryption_salt: str, encrypted_db_key: Optional[str] = None) -> Optional[int]:
        """
        Create a new user.
        
        Args:
            username: Unique username
            email: Unique email address
            password_hash: Hashed password (from bcrypt/argon2)
            encryption_salt: Salt for encryption key derivation
            encrypted_db_key: Optional encrypted database key for SQLCipher
        
        Returns:
            User ID if successful, None if username/email already exists
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, encryption_salt, encrypted_db_key)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, password_hash, encryption_salt, encrypted_db_key))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
            
        except sqlite3.IntegrityError:
            # Username or email already exists
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, encryption_salt, 
                   encrypted_db_key, is_active, created_at, last_login
            FROM users
            WHERE id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user by username.
        
        Args:
            username: Username
        
        Returns:
            User dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, encryption_salt, 
                   encrypted_db_key, is_active, created_at, last_login
            FROM users
            WHERE username = ?
        """, (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.
        
        Args:
            email: Email address
        
        Returns:
            User dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, encryption_salt, 
                   encrypted_db_key, is_active, created_at, last_login
            FROM users
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def update_last_login(self, user_id: int) -> bool:
        """
        Update user's last login timestamp.
        
        Args:
            user_id: User ID
        
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def deactivate(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id: User ID
        
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users
                SET is_active = 0
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def activate(self, user_id: int) -> bool:
        """
        Activate a user account.
        
        Args:
            user_id: User ID
        
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users
                SET is_active = 1
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def update_password(self, user_id: int, new_password_hash: str) -> bool:
        """
        Update user's password hash.
        
        Args:
            user_id: User ID
            new_password_hash: New hashed password
        
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users
                SET password_hash = ?
                WHERE id = ?
            """, (new_password_hash, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def count(self) -> int:
        """
        Get total number of users.
        
        Returns:
            Number of users
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            User dictionary if authentication successful, None otherwise
        """
        # Get user by username
        user = self.get_by_username(username)
        
        if not user:
            return None
        
        # Check if user is active
        if not user.get('is_active', 0):
            return None
        
        # Verify password
        password_hash = user.get('password_hash')
        if not password_hash:
            return None
        
        if not PasswordService.verify_password(password, password_hash):
            return None
        
        # Update last login
        self.update_last_login(user['id'])
        
        # Return user (without password hash for security)
        user_dict = dict(user)
        # Don't return password_hash in authenticated user
        user_dict.pop('password_hash', None)
        return user_dict
    
    def create_with_password(self, username: str, email: str, password: str,
                            encrypted_db_key: Optional[str] = None) -> Tuple[Optional[int], Optional[str]]:
        """
        Create a new user with password (handles hashing automatically).
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            encrypted_db_key: Optional encrypted database key for SQLCipher
        
        Returns:
            Tuple of (user_id, error_message)
            - user_id: User ID if successful, None if failed
            - error_message: None if successful, error description if failed
        """
        # Validate password strength
        is_valid, error_msg = PasswordService.validate_password_strength(password)
        if not is_valid:
            return None, error_msg
        
        # Hash password
        password_hash = PasswordService.hash_password(password)
        
        # Generate encryption salt
        encryption_salt = PasswordService.generate_salt()
        
        # Create user
        user_id = self.create(username, email, password_hash, encryption_salt, encrypted_db_key)
        
        if user_id:
            return user_id, None
        else:
            return None, "Username or email already exists"