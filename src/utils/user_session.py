"""
User Session Utilities
Flask-Login compatible user class wrapper
"""

from flask_login import UserMixin
from typing import Optional, Dict, Any
import sys
import os

# Add models to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.user import User as UserModel


class UserSession(UserMixin):
    """
    Flask-Login compatible user class.
    Wraps the User model to work with Flask-Login.
    """
    
    def __init__(self, user_data: Dict[str, Any], db_path: str):
        """
        Initialize user session from user data.
        
        Args:
            user_data: User dictionary from database
            db_path: Path to database
        """
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.is_active = bool(user_data.get('is_active', 1))
        self.created_at = user_data.get('created_at')
        self.last_login = user_data.get('last_login')
        self.encryption_salt = user_data.get('encryption_salt')
        self._db_path = db_path
    
    def get_id(self) -> str:
        """Return user ID as string (required by Flask-Login)."""
        return str(self.id)
    
    @staticmethod
    def get_by_id(user_id: int, db_path: str) -> Optional['UserSession']:
        """
        Load user by ID for Flask-Login.
        
        Args:
            user_id: User ID
            db_path: Path to database
        
        Returns:
            UserSession instance or None
        """
        user_model = UserModel(db_path)
        user_data = user_model.get_by_id(user_id)
        
        if user_data and user_data.get('is_active', 0):
            return UserSession(user_data, db_path)
        return None
    
    @staticmethod
    def authenticate(username: str, password: str, db_path: str) -> Optional['UserSession']:
        """
        Authenticate user and return UserSession if successful.
        
        Args:
            username: Username
            password: Plain text password
            db_path: Path to database
        
        Returns:
            UserSession instance or None
        """
        user_model = UserModel(db_path)
        user_data = user_model.authenticate(username, password)
        
        if user_data:
            return UserSession(user_data, db_path)
        return None
