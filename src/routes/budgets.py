"""
Budgets Blueprint
Handles routes for budget management
"""

from flask import Blueprint, render_template, jsonify, request, current_app
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.budget import Budget
from services.budget_service import BudgetService

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')


@budgets_bp.route('/')
def budgets_page():
    """Display the budgets management page"""
    return render_template('budgets.html')


@budgets_bp.route('/api/')
def get_all_budgets():
    """Get all budgets with progress"""
    try:
        period_type = request.args.get('period_type', 'monthly')
        
        budget_service = BudgetService(current_app.config['DATABASE'])
        progress_list = budget_service.get_all_budgets_progress(period_type)
        summary = budget_service.get_budget_summary()
        
        return jsonify({
            'success': True,
            'budgets': progress_list,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@budgets_bp.route('/api/create', methods=['POST'])
def create_budget():
    """Create a new budget"""
    try:
        data = request.get_json()
        
        budget_model = Budget(current_app.config['DATABASE'])
        budget_id = budget_model.create(
            category_id=data['category_id'],
            amount=float(data['amount']),
            period_type=data.get('period_type', 'monthly'),
            start_date=data['start_date'],
            end_date=data['end_date'],
            alert_threshold=int(data.get('alert_threshold', 80))
        )
        
        return jsonify({
            'success': True,
            'budget_id': budget_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@budgets_bp.route('/api/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    """Update an existing budget"""
    try:
        data = request.get_json()
        
        budget_model = Budget(current_app.config['DATABASE'])
        success = budget_model.update(budget_id, **data)
        
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@budgets_bp.route('/api/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    """Delete a budget"""
    try:
        budget_model = Budget(current_app.config['DATABASE'])
        success = budget_model.delete(budget_id)
        
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@budgets_bp.route('/api/summary')
def get_budget_summary():
    """Get budget summary statistics"""
    try:
        budget_service = BudgetService(current_app.config['DATABASE'])
        summary = budget_service.get_budget_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@budgets_bp.route('/api/charts/category')
def get_budget_category_chart():
    """Return budget vs actual data by category."""
    try:
        period_type = request.args.get('period_type', 'monthly')
        budget_service = BudgetService(current_app.config['DATABASE'])
        data = budget_service.get_category_variance(period_type)
        return jsonify({'success': True, **data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@budgets_bp.route('/api/charts/trend')
def get_budget_trend_chart():
    """Return budget performance trend over recent months."""
    try:
        period_type = request.args.get('period_type', 'monthly')
        months = int(request.args.get('months', 6))
        budget_service = BudgetService(current_app.config['DATABASE'])
        data = budget_service.get_monthly_performance(months, period_type)
        return jsonify({'success': True, **data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

