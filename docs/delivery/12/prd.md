# PBI-12: User Authentication & Encrypted Data Storage

**Status**: Proposed  
**Priority**: High  
**Complexity**: High  
**Owner**: Saeed  
**Created**: 2026-01-13  

[View in Backlog](../backlog.md#user-content-12)

---

## Overview

Implement secure user authentication and authorization with encrypted data storage, ensuring each user's financial data is isolated and protected. This feature transforms the application from single-user to multi-user with enterprise-grade security.

## Problem Statement

Currently, the application operates as a single-user system with no authentication. All data is stored in plain text in a single SQLite database. This creates security risks:
- No access control
- No data isolation
- No encryption at rest
- Vulnerable to unauthorized access
- Cannot support multiple users

## User Stories

- **As a user**, I want to create an account with a secure password so that my financial data is protected.
- **As a user**, I want to log in securely so that only I can access my financial data.
- **As a user**, I want my data encrypted so that even if someone gains access to the database, they cannot read my financial information.
- **As a user**, I want my data isolated from other users so that privacy is maintained.
- **As a user**, I want secure session management so that my session doesn't expire unexpectedly and unauthorized users can't access my account.

## Technical Approach

### 1. Authentication System

**Password Security:**
- Use `bcrypt` or `argon2` for password hashing (never store plain text)
- Enforce strong password policies (min length, complexity)
- Implement password reset functionality
- Rate limiting on login attempts

**Session Management:**
- Use Flask-Login for session management
- Secure session cookies (HttpOnly, Secure, SameSite)
- Session timeout after inactivity
- CSRF protection

**User Model:**
- Create `users` table with: id, username, email, password_hash, created_at, last_login, is_active
- Unique constraints on username and email
- Support for user roles (admin, user) for future expansion

### 2. Data Isolation (Multi-Tenancy)

**Approach: Row-Level Security**
- Add `user_id` foreign key to all data tables:
  - `accounts` → `user_id`
  - `transactions` → `user_id` (via account)
  - `categories` → `user_id` (with shared system categories)
  - `budgets` → `user_id`
  - `goals` → `user_id`
  - `tags` → `user_id`
  - `categorization_rules` → `user_id` (with shared system rules)
  - `recurring_transactions` → `user_id`

**Query Filtering:**
- All queries automatically filter by `current_user.id`
- Middleware/decorator to enforce user context
- Prevent cross-user data access

### 3. Encryption Strategy

**Option A: Application-Level Encryption (Recommended)**
- Encrypt sensitive fields using AES-256-GCM
- Use user-specific encryption keys derived from password
- Encrypt: account numbers, transaction descriptions, notes, tags
- Keep amounts and dates unencrypted for querying/aggregation

**Option B: Database-Level Encryption**
- Use SQLCipher (encrypted SQLite)
- Encrypt entire database with master key
- Requires separate database per user OR master key management

**Recommended: Hybrid Approach**
- Use SQLCipher for database file encryption
- Additional application-level encryption for highly sensitive fields
- Key derivation from user password + salt

### 4. Key Management

**User Encryption Keys:**
- Derive encryption key from user password using PBKDF2
- Store salt in user record (not password salt)
- Key derivation: `PBKDF2(password, salt, iterations=100000)`
- Never store encryption keys in plain text

**Master Key (for SQLCipher):**
- Generate per-user database encryption key
- Encrypt master key with user's derived key
- Store encrypted master key in user record

### 5. Database Schema Changes

**New Tables:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    encryption_salt TEXT NOT NULL,
    encrypted_db_key TEXT,  -- For SQLCipher
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Modified Tables:**
- Add `user_id` to all data tables
- Add indexes on `user_id` for performance
- Migration script to handle existing single-user data

### 6. Security Best Practices

**Password Requirements:**
- Minimum 12 characters
- Require uppercase, lowercase, numbers, special characters
- Password strength meter
- Prevent common passwords

**Session Security:**
- HttpOnly cookies (prevent XSS)
- Secure flag (HTTPS only)
- SameSite=Strict (prevent CSRF)
- Session timeout: 30 minutes inactivity
- Maximum session duration: 24 hours

**Rate Limiting:**
- 5 login attempts per 15 minutes
- Account lockout after 10 failed attempts
- IP-based rate limiting

**Audit Logging:**
- Log all authentication events
- Log data access patterns
- Security event monitoring

## UX/UI Considerations

**Login/Registration:**
- Clean, simple login page
- Registration form with password strength indicator
- "Remember me" option (extended session)
- Password reset flow
- Clear error messages (don't reveal if username exists)

**User Management:**
- User profile page
- Change password functionality
- Account deletion (with data export option)
- Session management (view active sessions, logout all)

**Migration Experience:**
- On first launch after upgrade, prompt to create admin account
- Migrate existing data to first user
- Clear migration instructions

## Acceptance Criteria

### Must Have
- [ ] User registration with secure password hashing
- [ ] Login/logout functionality
- [ ] Session management with Flask-Login
- [ ] All data tables include `user_id` foreign key
- [ ] All queries filter by current user
- [ ] Application-level encryption for sensitive fields
- [ ] Password reset functionality
- [ ] Secure session cookies (HttpOnly, Secure, SameSite)
- [ ] Rate limiting on authentication endpoints
- [ ] Migration script for existing single-user data

### Should Have
- [ ] SQLCipher database encryption
- [ ] Password strength meter
- [ ] "Remember me" functionality
- [ ] User profile management
- [ ] Active session viewing
- [ ] Account deletion with data export
- [ ] Audit logging for security events

### Could Have
- [ ] Multi-factor authentication (MFA)
- [ ] OAuth/SSO integration
- [ ] Admin user management interface
- [ ] User roles and permissions
- [ ] Password expiration policies
- [ ] Security dashboard

## Dependencies

- Flask-Login for session management
- bcrypt or argon2-cffi for password hashing
- cryptography library for encryption
- SQLCipher for database encryption (optional but recommended)
- Flask-WTF for CSRF protection

## Security Considerations

**Critical Security Requirements:**
1. **Never store passwords in plain text** - Always hash with bcrypt/Argon2
2. **Encrypt sensitive data at rest** - Use AES-256-GCM
3. **Secure key management** - Derive keys from passwords, never store plain keys
4. **Prevent SQL injection** - Use parameterized queries (already done)
5. **CSRF protection** - Use Flask-WTF tokens
6. **XSS prevention** - Sanitize user input, use template escaping
7. **Session hijacking prevention** - Secure cookies, session rotation
8. **Rate limiting** - Prevent brute force attacks

**Threat Model:**
- **Unauthorized access** - Mitigated by authentication
- **Data breach** - Mitigated by encryption
- **Session hijacking** - Mitigated by secure cookies
- **Brute force** - Mitigated by rate limiting
- **SQL injection** - Already mitigated
- **XSS** - Mitigated by template escaping

## Implementation Phases

### Phase 1: Core Authentication (Foundation)
- User model and database schema
- Registration and login endpoints
- Password hashing
- Basic session management
- User context middleware

### Phase 2: Data Isolation
- Add `user_id` to all tables
- Update all queries to filter by user
- Migration script for existing data
- Testing data isolation

### Phase 3: Encryption
- Implement application-level encryption
- Key derivation from passwords
- Encrypt sensitive fields
- Testing encryption/decryption

### Phase 4: Security Hardening
- Rate limiting
- CSRF protection
- Secure cookies
- Password policies
- Audit logging

### Phase 5: Advanced Features (Optional)
- SQLCipher integration
- MFA support
- Admin interface
- User management

## Open Questions

1. **Encryption Approach**: Application-level vs SQLCipher vs both?
   - **Recommendation**: Start with application-level, add SQLCipher later if needed

2. **Password Reset**: Email-based or security questions?
   - **Recommendation**: Email-based (requires email service integration)

3. **Existing Data**: How to handle current single-user database?
   - **Recommendation**: Migrate to first registered user

4. **Shared Categories/Rules**: Should system categories be shared or per-user?
   - **Recommendation**: Shared system categories, user can create custom ones

5. **Performance**: Will encryption impact query performance?
   - **Recommendation**: Encrypt only sensitive fields, keep amounts/dates unencrypted for queries

## Related Tasks

- [Tasks for PBI 12](./tasks.md)

---

## Technical Notes

### Encryption Implementation Example

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_field(data: str, user_key: bytes) -> str:
    """Encrypt sensitive field"""
    f = Fernet(user_key)
    encrypted = f.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_field(encrypted_data: str, user_key: bytes) -> str:
    """Decrypt sensitive field"""
    f = Fernet(user_key)
    decrypted = f.decrypt(base64.urlsafe_b64decode(encrypted_data))
    return decrypted.decode()
```

### Session Management Example

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/login', methods=['POST'])
def login():
    user = User.authenticate(username, password)
    if user:
        login_user(user, remember=remember_me)
        return redirect('/dashboard')
    return render_template('login.html', error='Invalid credentials')
```
