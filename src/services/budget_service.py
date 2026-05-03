"""
Budget Service
Calculates budget progress, alerts, and analysis
"""

import sqlite3
from typing import List, Dict, Any
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class BudgetService:
    """Service for budget calculations and progress tracking"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_budget_progress(self, budget_id: int) -> Dict[str, Any]:
        """
        Calculate progress for a specific budget.
        
        Returns: {
            "budget_id": 1,
            "category_name": "Groceries",
            "budgeted": 800.00,
            "actual": 654.32,
            "remaining": 145.68,
            "percentage": 81.79,
            "status": "warning",  # "good", "warning", "over"
            "alert": False
        }
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get budget details
        cursor.execute("""
            SELECT b.*, c.name as category_name
            FROM budgets b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.id = ?
        """, (budget_id,))
        
        budget = cursor.fetchone()
        if not budget:
            conn.close()
            return None
        
        # Calculate actual spending
        cursor.execute("""
            SELECT SUM(ABS(amount)) as total
            FROM transactions
            WHERE category_id = ?
            AND amount < 0
            AND date >= ?
            AND date <= ?
        """, (budget['category_id'], budget['start_date'], budget['end_date']))
        
        result = cursor.fetchone()
        actual = float(result['total']) if result['total'] else 0.0
        
        conn.close()
        
        budgeted = float(budget['amount'])
        remaining = budgeted - actual
        percentage = (actual / budgeted * 100) if budgeted > 0 else 0.0
        
        # Determine status
        if percentage >= 100:
            status = 'over'
        elif percentage >= budget['alert_threshold']:
            status = 'warning'
        else:
            status = 'good'
        
        return {
            'budget_id': budget['id'],
            'category_id': budget['category_id'],
            'category_name': budget['category_name'],
            'budgeted': round(budgeted, 2),
            'actual': round(actual, 2),
            'remaining': round(remaining, 2),
            'percentage': round(percentage, 1),
            'status': status,
            'alert': percentage >= budget['alert_threshold'],
            'period_type': budget['period_type'],
            'start_date': budget['start_date'],
            'end_date': budget['end_date']
        }
    
    def get_all_budgets_progress(self, period_type: str = 'monthly') -> List[Dict[str, Any]]:
        """Get progress for all budgets"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get all budgets for the current period
        today = date.today().isoformat()
        
        cursor.execute("""
            SELECT id FROM budgets
            WHERE period_type = ?
            AND start_date <= ?
            AND end_date >= ?
            ORDER BY id ASC
        """, (period_type, today, today))
        
        budget_ids = [row['id'] for row in cursor.fetchall()]
        conn.close()
        
        # Calculate progress for each
        progress_list = []
        for budget_id in budget_ids:
            progress = self.get_budget_progress(budget_id)
            if progress:
                progress_list.append(progress)
        
        return progress_list
    
    def get_budget_summary(self) -> Dict[str, Any]:
        """
        Get overall budget summary.
        
        Returns: {
            "total_budgeted": 5000.00,
            "total_actual": 3245.67,
            "total_remaining": 1754.33,
            "budgets_count": 5,
            "over_budget_count": 1,
            "at_risk_count": 2
        }
        """
        progress_list = self.get_all_budgets_progress()
        
        total_budgeted = sum(p['budgeted'] for p in progress_list)
        total_actual = sum(p['actual'] for p in progress_list)
        total_remaining = total_budgeted - total_actual
        over_budget_count = sum(1 for p in progress_list if p['status'] == 'over')
        at_risk_count = sum(1 for p in progress_list if p['status'] == 'warning')
        
        return {
            'total_budgeted': round(total_budgeted, 2),
            'total_actual': round(total_actual, 2),
            'total_remaining': round(total_remaining, 2),
            'budgets_count': len(progress_list),
            'over_budget_count': over_budget_count,
            'at_risk_count': at_risk_count
        }

    def get_category_variance(self, period_type: str = 'monthly') -> Dict[str, Any]:
        """
        Build data series for budget vs actual comparison by category.
        """
        progress_list = self.get_all_budgets_progress(period_type)

        labels: List[str] = []
        budgeted: List[float] = []
        actual: List[float] = []
        variance: List[float] = []
        statuses: List[str] = []

        for entry in progress_list:
            labels.append(entry['category_name'])
            budgeted.append(round(entry['budgeted'], 2))
            actual.append(round(entry['actual'], 2))
            diff = round(entry['actual'] - entry['budgeted'], 2)
            variance.append(diff)
            statuses.append(entry['status'])

        return {
            'labels': labels,
            'budgeted': budgeted,
            'actual': actual,
            'variance': variance,
            'statuses': statuses
        }

    def get_monthly_performance(self, months: int = 6, period_type: str = 'monthly') -> Dict[str, Any]:
        """
        Build time-series data for budget performance across recent months.
        """
        months = max(1, months)
        labels: List[str] = []
        budgeted_series: List[float] = []
        actual_series: List[float] = []
        variance_series: List[float] = []

        today = date.today().replace(day=1)

        for offset in range(months - 1, -1, -1):
            month_start = today - relativedelta(months=offset)
            month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)

            month_budgets = self._get_budgets_for_period(month_start, month_end, period_type)

            total_budgeted = 0.0
            total_actual = 0.0

            for budget in month_budgets:
                amount = float(budget['amount'])
                total_budgeted += amount
                total_actual += self._calculate_actual_spending(
                    budget['category_id'],
                    month_start,
                    month_end
                )

            labels.append(month_start.strftime('%b %Y'))
            budgeted_series.append(round(total_budgeted, 2))
            actual_series.append(round(total_actual, 2))
            variance_series.append(round(total_actual - total_budgeted, 2))

        return {
            'labels': labels,
            'budgeted': budgeted_series,
            'actual': actual_series,
            'variance': variance_series
        }

    def _get_budgets_for_period(self, start_date: date, end_date: date, period_type: str) -> List[Dict[str, Any]]:
        """Return budgets that overlap a given period."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT b.*, c.name as category_name
            FROM budgets b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.period_type = ?
              AND b.start_date <= ?
              AND b.end_date >= ?
            """,
            (period_type, end_date.isoformat(), start_date.isoformat()),
        )

        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def _calculate_actual_spending(self, category_id: int, start_date: date, end_date: date) -> float:
        """Calculate actual spending for category within period."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT SUM(ABS(amount)) AS total
            FROM transactions
            WHERE category_id = ?
              AND amount < 0
              AND date >= ?
              AND date <= ?
            """,
            (category_id, start_date.isoformat(), end_date.isoformat()),
        )
        result = cursor.fetchone()
        conn.close()
        return float(result['total']) if result['total'] else 0.0

