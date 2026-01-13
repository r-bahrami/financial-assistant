"""Financial Health Dashboard Routes"""
from flask import Blueprint, render_template, jsonify, current_app
import sqlite3
from datetime import date, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def calculate_health_score(savings_rate: float, total_balance: float, total_budgets: int, net_income: float) -> int:
    """Calculate the dashboard health score based on key financial metrics."""
    score = 0

    if savings_rate > 20:
        score += 40
    elif savings_rate > 10:
        score += 30
    elif savings_rate > 0:
        score += 20

    if total_balance > 5000:
        score += 30
    elif total_balance > 1000:
        score += 20
    elif total_balance > 0:
        score += 10

    if total_budgets > 0:
        score += 20

    if net_income > 0:
        score += 10

    return min(100, score)

@dashboard_bp.route('/')
def dashboard_page():
    return render_template('dashboard.html', app_name='Financial Assistant')

@dashboard_bp.route('/api/health')
def get_financial_health():
    """Get comprehensive financial health metrics"""
    try:
        conn = sqlite3.connect(current_app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Net income (last 30 days)
        thirty_days_ago = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN amount > 0 AND c.type != 'transfer' THEN amount ELSE 0 END), 0) as income,
                COALESCE(SUM(CASE WHEN amount < 0 AND c.type != 'transfer' THEN ABS(amount) ELSE 0 END), 0) as expenses
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.date >= ?
        """, (thirty_days_ago,))
        
        row = cursor.fetchone()
        income_30d = row['income']
        expenses_30d = row['expenses']
        net_income = income_30d - expenses_30d
        savings_rate = (net_income / income_30d * 100) if income_30d > 0 else 0
        
        # Budget compliance
        cursor.execute("SELECT COUNT(*) as total FROM budgets")
        total_budgets = cursor.fetchone()['total']
        
        # Top categories (last 30 days) - exclude transfers
        cursor.execute("""
            SELECT c.name, SUM(ABS(t.amount)) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.date >= ? AND t.amount < 0 AND c.type != 'transfer'
            GROUP BY c.name
            ORDER BY total DESC
            LIMIT 5
        """, (thirty_days_ago,))
        
        top_categories = [dict(row) for row in cursor.fetchall()]
        
        # Account balances
        cursor.execute("SELECT SUM(current_balance) as total FROM accounts")
        total_balance = cursor.fetchone()['total'] or 0
        
        conn.close()
        
        # Calculate health score (0-100)
        health_score = calculate_health_score(savings_rate, total_balance, total_budgets, net_income)
        
        return jsonify({
            'success': True,
            'health': {
                'income_30d': round(income_30d, 2),
                'expenses_30d': round(expenses_30d, 2),
                'net_income': round(net_income, 2),
                'savings_rate': round(savings_rate, 1),
                'total_balance': round(total_balance, 2),
                'budget_count': total_budgets,
                'top_categories': top_categories,
                'health_score': min(100, health_score)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
