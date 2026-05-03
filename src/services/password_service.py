"""
Password Service
Handles password hashing, verification, and strength validation
"""

import bcrypt
import secrets
import re
from typing import Tuple, Optional


class PasswordService:
    """Service for password operations."""
    
    # Password requirements
    MIN_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_NUMBER = True
    REQUIRE_SPECIAL = True
    
    # Bcrypt cost factor (higher = more secure but slower)
    # 12 rounds = ~300ms on modern hardware, good balance
    BCRYPT_ROUNDS = 12
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password string
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=PasswordService.BCRYPT_ROUNDS)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Stored password hash
        
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def generate_salt(length: int = 32) -> str:
        """
        Generate a secure random salt for encryption key derivation.
        
        Args:
            length: Length of salt in bytes (default: 32)
        
        Returns:
            Hex-encoded salt string
        """
        return secrets.token_hex(length)
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength against requirements.
        
        Args:
            password: Password to validate
        
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if password meets requirements
            - error_message: None if valid, error description if invalid
        """
        if not password:
            return False, "Password cannot be empty"
        
        # Check minimum length
        if len(password) < PasswordService.MIN_LENGTH:
            return False, f"Password must be at least {PasswordService.MIN_LENGTH} characters long"
        
        # Check for uppercase
        if PasswordService.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for lowercase
        if PasswordService.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for number
        if PasswordService.REQUIRE_NUMBER and not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        # Check for special character
        if PasswordService.REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
        
        # Check for common weak passwords
        common_passwords = [
            'password', '12345678', 'qwerty', 'abc123', 'password123',
            'admin', 'letmein', 'welcome', 'monkey', '1234567890'
        ]
        if password.lower() in common_passwords:
            return False, "Password is too common. Please choose a more unique password"
        
        return True, None
    
    @staticmethod
    def get_password_strength_score(password: str) -> int:
        """
        Calculate password strength score (0-100).
        
        Args:
            password: Password to score
        
        Returns:
            Strength score from 0-100
        """
        score = 0
        
        # Length scoring (max 40 points)
        if len(password) >= 12:
            score += 20
        if len(password) >= 16:
            score += 10
        if len(password) >= 20:
            score += 10
        
        # Character variety (max 40 points)
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 10
        
        # Complexity bonus (max 20 points)
        if len(set(password)) >= len(password) * 0.7:  # 70% unique characters
            score += 10
        if len(password) >= 16 and len(set(password)) >= 12:
            score += 10
        
        return min(100, score)
