"""
Admin routes for database management.
"""

from flask import Blueprint, request, jsonify, render_template, current_app, abort
from flask_login import login_required, current_user
import sqlite3
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.user_session import UserSession

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin role."""
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # Unauthorized
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def admin_page():
    """Render the admin management page."""
    return render_template('admin.html', current_user_id=current_user.id)


@admin_bp.route('/api/reset-database', methods=['POST'])
@admin_required
def reset_database():
    """
    Reset the database by deleting all transactions and accounts.
    Requires confirmation token.
    
    Request JSON:
        {
            "confirmation": "DELETE ALL DATA",
            "reset_type": "all" | "transactions"
        }
    
    Returns:
        JSON with success status and counts
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Require exact confirmation text
    confirmation = data.get('confirmation', '').strip()
    if confirmation != 'DELETE ALL DATA':
        return jsonify({
            'success': False,
            'error': 'Invalid confirmation text. You must type exactly: DELETE ALL DATA'
        }), 400
    
    reset_type = data.get('reset_type', 'all')
    
    if reset_type not in ['all', 'transactions']:
        return jsonify({
            'success': False,
            'error': 'Invalid reset_type. Must be "all" or "transactions"'
        }), 400
    
    try:
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Count before deletion
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM accounts")
        account_count = cursor.fetchone()[0]
        
        # Delete data based on reset_type
        if reset_type == 'all':
            # Delete all transactions first (due to foreign key)
            cursor.execute("DELETE FROM transactions")
            # Delete all accounts
            cursor.execute("DELETE FROM accounts")
            # Reset auto-increment counters
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts'")
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'Database reset complete. Deleted {transaction_count} transactions and {account_count} accounts.',
                'transactions_deleted': transaction_count,
                'accounts_deleted': account_count
            })
        
        else:  # transactions only
            cursor.execute("DELETE FROM transactions")
            # Reset auto-increment counter
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'Transactions reset complete. Deleted {transaction_count} transactions. Kept {account_count} accounts.',
                'transactions_deleted': transaction_count,
                'accounts_deleted': 0
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Database reset failed: {str(e)}'
        }), 500


@admin_bp.route('/api/stats', methods=['GET'])
@admin_required
def get_stats():
    """Get database statistics."""
    try:
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM accounts")
        account_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        
        # Get database file size
        db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        db_size_mb = db_size / (1024 * 1024)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'transactions': transaction_count,
                'accounts': account_count,
                'categories': category_count,
                'database_size_mb': round(db_size_mb, 2)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get stats: {str(e)}'
        }), 500


@admin_bp.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)."""
    try:
        db_path = current_app.config['DATABASE']
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from models.user import User
        
        user_model = User(db_path)
        users = user_model.get_all()
        
        return jsonify({
            'success': True,
            'users': users
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get users: {str(e)}'
        }), 500


@admin_bp.route('/api/users/<int:user_id>/activate', methods=['POST'])
@admin_required
def activate_user(user_id):
    """Activate a user account."""
    try:
        db_path = current_app.config['DATABASE']
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from models.user import User
        
        user_model = User(db_path)
        success = user_model.activate(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User activated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'User not found or activation failed'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to activate user: {str(e)}'
        }), 500


@admin_bp.route('/api/users/<int:user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    """Deactivate a user account."""
    try:
        # Prevent deactivating yourself
        if user_id == current_user.id:
            return jsonify({
                'success': False,
                'error': 'Cannot deactivate your own account'
            }), 400
        
        db_path = current_app.config['DATABASE']
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from models.user import User
        
        user_model = User(db_path)
        success = user_model.deactivate(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User deactivated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'User not found or deactivation failed'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to deactivate user: {str(e)}'
        }), 500


@admin_bp.route('/api/users/<int:user_id>/delete', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user account."""
    try:
        # Prevent deleting yourself
        if user_id == current_user.id:
            return jsonify({
                'success': False,
                'error': 'Cannot delete your own account'
            }), 400
        
        db_path = current_app.config['DATABASE']
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from models.user import User
        
        user_model = User(db_path)
        success = user_model.delete(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'User deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'User not found or deletion failed'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete user: {str(e)}'
        }), 500


@admin_bp.route('/api/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    """Update a user's role."""
    try:
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['admin', 'user']:
            return jsonify({
                'success': False,
                'error': 'Invalid role. Must be "admin" or "user"'
            }), 400
        
        db_path = current_app.config['DATABASE']
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from models.user import User
        
        user_model = User(db_path)
        success = user_model.update_role(user_id, new_role)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'User role updated to {new_role}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'User not found or update failed'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update role: {str(e)}'
        }), 500

