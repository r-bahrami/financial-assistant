"""
Authentication Routes
Handles user login, logout, and registration
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.user import User
from utils.user_session import UserSession
from services.password_service import PasswordService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'GET':
        # If already logged in, redirect to dashboard
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard_page'))
        return render_template('auth/login.html')
    
    # POST request - process login
    data = request.get_json() if request.is_json else request.form
    username = data.get('username', '').strip()
    password = data.get('password', '')
    remember_me = data.get('remember_me', False)
    
    if not username or not password:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Username and password are required'}), 400
        flash('Username and password are required', 'error')
        return render_template('auth/login.html', error='Username and password are required')
    
    # Get database path from app config
    from flask import current_app
    db_path = current_app.config['DATABASE']
    
    # Authenticate user
    user_session = UserSession.authenticate(username, password, db_path)
    
    if user_session:
        # Login successful
        login_user(user_session, remember=remember_me, duration=timedelta(hours=24) if remember_me else timedelta(minutes=30))
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user_session.id,
                    'username': user_session.username,
                    'email': user_session.email
                }
            })
        
        # Redirect to dashboard or next page
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.dashboard_page'))
    else:
        # Login failed
        if request.is_json:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
        flash('Invalid username or password', 'error')
        return render_template('auth/login.html', error='Invalid username or password')


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'GET':
        # If already logged in, redirect to dashboard
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard_page'))
        return render_template('auth/register.html')
    
    # POST request - process registration
    data = request.get_json() if request.is_json else request.form
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    password_confirm = data.get('password_confirm', '')
    
    # Validation
    errors = []
    
    if not username:
        errors.append('Username is required')
    elif len(username) < 3:
        errors.append('Username must be at least 3 characters')
    elif len(username) > 50:
        errors.append('Username must be less than 50 characters')
    
    if not email:
        errors.append('Email is required')
    elif '@' not in email:
        errors.append('Invalid email format')
    
    if not password:
        errors.append('Password is required')
    elif password != password_confirm:
        errors.append('Passwords do not match')
    
    # Validate password strength
    if password:
        is_valid, error_msg = PasswordService.validate_password_strength(password)
        if not is_valid:
            errors.append(error_msg)
    
    if errors:
        if request.is_json:
            return jsonify({'success': False, 'errors': errors}), 400
        return render_template('auth/register.html', errors=errors)
    
    # Get database path from app config
    from flask import current_app
    db_path = current_app.config['DATABASE']
    
    # Create user
    user_model = User(db_path)
    user_id, error = user_model.create_with_password(username, email, password)
    
    if user_id:
        # Registration successful - auto-login
        user_data = user_model.get_by_id(user_id)
        user_session = UserSession(user_data, db_path)
        login_user(user_session, remember=False)
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'user': {
                    'id': user_session.id,
                    'username': user_session.username,
                    'email': user_session.email
                }
            }), 201
        
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('dashboard.dashboard_page'))
    else:
        # Registration failed
        error_msg = error or 'Registration failed. Username or email may already exist.'
        if request.is_json:
            return jsonify({'success': False, 'error': error_msg}), 400
        return render_template('auth/register.html', errors=[error_msg])


@auth_bp.route('/check')
def check_auth():
    """Check if user is authenticated (for API)."""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        })
    return jsonify({'authenticated': False})
