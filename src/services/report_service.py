"""
Report Service
Aggregates transaction data for financial reports and charts
"""

import sqlite3
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from flask import current_app


class ReportService:
    """Service for generating financial report data"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _format_date(self, date_obj) -> str:
        """Convert date object to string"""
        if isinstance(date_obj, str):
            return date_obj
        if isinstance(date_obj, (date, datetime)):
            return date_obj.strftime('%Y-%m-%d')
        return str(date_obj)
    
    def get_monthly_income_expenses(
        self,
        account_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """
        Get monthly income and expense totals.
        
        Returns: [
            {
                "month": "2025-01",
                "income": 5000.00,
                "expenses": 3500.00,
                "net": 1500.00
            },
            ...
        ]
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                strftime('%Y-%m', date) as month,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as expenses
            FROM transactions
            WHERE 1=1
        """
        params = []
        
        if account_id:
            query += " AND account_id = ?"
            params.append(account_id)
        
        if start_date:
            query += " AND date >= ?"
            params.append(self._format_date(start_date))
        
        if end_date:
            query += " AND date <= ?"
            params.append(self._format_date(end_date))
        
        query += """
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month ASC
        """
        
        cursor.execute(query, params)
        results = []
        
        for row in cursor.fetchall():
            income = float(row['income']) if row['income'] else 0.0
            expenses = float(row['expenses']) if row['expenses'] else 0.0
            results.append({
                'month': row['month'],
                'income': round(income, 2),
                'expenses': round(expenses, 2),
                'net': round(income - expenses, 2)
            })
        
        conn.close()
        return results
    
    def get_category_breakdown(
        self,
        account_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """
        Get spending breakdown by category.
        
        Returns: [
            {
                "category": "Groceries",
                "amount": 850.25,
                "percentage": 24.3,
                "transaction_count": 45
            },
            ...
        ]
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # First, get total expenses for percentage calculation (exclude transfers)
        total_query = """
            SELECT SUM(ABS(t.amount)) as total
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.amount < 0 AND (c.type IS NULL OR c.type != 'transfer')
        """
        total_params = []
        
        if account_id:
            total_query += " AND t.account_id = ?"
            total_params.append(account_id)
        
        if start_date:
            total_query += " AND t.date >= ?"
            total_params.append(self._format_date(start_date))
        
        if end_date:
            total_query += " AND t.date <= ?"
            total_params.append(self._format_date(end_date))
        
        cursor.execute(total_query, total_params)
        total_row = cursor.fetchone()
        total_expenses = float(total_row['total']) if total_row['total'] else 0.0
        
        # Now get category breakdown (exclude transfers)
        query = """
            SELECT 
                COALESCE(c.name, 'Uncategorized') as category,
                SUM(ABS(t.amount)) as amount,
                COUNT(t.id) as transaction_count
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.amount < 0 AND (c.type IS NULL OR c.type != 'transfer')
        """
        params = []
        
        if account_id:
            query += " AND t.account_id = ?"
            params.append(account_id)
        
        if start_date:
            query += " AND t.date >= ?"
            params.append(self._format_date(start_date))
        
        if end_date:
            query += " AND t.date <= ?"
            params.append(self._format_date(end_date))
        
        query += """
            GROUP BY c.name
            ORDER BY amount DESC
        """
        
        cursor.execute(query, params)
        results = []
        
        for row in cursor.fetchall():
            amount = float(row['amount']) if row['amount'] else 0.0
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0.0
            results.append({
                'category': row['category'],
                'amount': round(amount, 2),
                'percentage': round(percentage, 1),
                'transaction_count': row['transaction_count']
            })
        
        conn.close()
        return results
    
    def get_monthly_category_trends(
        self,
        account_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Get monthly expenses broken down by category.
        
        Returns: {
            "months": ["2025-01", "2025-02", ...],
            "categories": {
                "Groceries": [850, 920, 880, ...],
                "Rent": [2000, 2000, 2000, ...],
                ...
            }
        }
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get top N categories by total spending (exclude transfers)
        top_categories_query = """
            SELECT 
                COALESCE(c.name, 'Uncategorized') as category,
                SUM(ABS(t.amount)) as total
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.amount < 0 AND (c.type IS NULL OR c.type != 'transfer')
        """
        top_params = []
        
        if account_id:
            top_categories_query += " AND t.account_id = ?"
            top_params.append(account_id)
        
        if start_date:
            top_categories_query += " AND t.date >= ?"
            top_params.append(self._format_date(start_date))
        
        if end_date:
            top_categories_query += " AND t.date <= ?"
            top_params.append(self._format_date(end_date))
        
        top_categories_query += f"""
            GROUP BY c.name
            ORDER BY total DESC
            LIMIT {top_n}
        """
        
        cursor.execute(top_categories_query, top_params)
        top_categories = [row['category'] for row in cursor.fetchall()]
        
        # Get all unique months
        months_query = """
            SELECT DISTINCT strftime('%Y-%m', date) as month
            FROM transactions
            WHERE amount < 0
        """
        months_params = []
        
        if account_id:
            months_query += " AND account_id = ?"
            months_params.append(account_id)
        
        if start_date:
            months_query += " AND date >= ?"
            months_params.append(self._format_date(start_date))
        
        if end_date:
            months_query += " AND date <= ?"
            months_params.append(self._format_date(end_date))
        
        months_query += " ORDER BY month ASC"
        
        cursor.execute(months_query, months_params)
        months = [row['month'] for row in cursor.fetchall()]
        
        # Get data for each category and month
        categories_data = {}
        
        for category in top_categories:
            category_data = []
            
            for month in months:
                query = """
                    SELECT SUM(ABS(t.amount)) as amount
                    FROM transactions t
                    LEFT JOIN categories c ON t.category_id = c.id
                    WHERE t.amount < 0
                    AND strftime('%Y-%m', t.date) = ?
                    AND COALESCE(c.name, 'Uncategorized') = ?
                """
                params = [month, category]
                
                if account_id:
                    query += " AND t.account_id = ?"
                    params.append(account_id)
                
                cursor.execute(query, params)
                row = cursor.fetchone()
                amount = float(row['amount']) if row['amount'] else 0.0
                category_data.append(round(amount, 2))
            
            categories_data[category] = category_data
        
        conn.close()
        
        return {
            'months': months,
            'categories': categories_data
        }
    
    def get_top_categories(
        self,
        account_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get top spending categories.
        
        Returns: [
            {
                "category": "Rent",
                "amount": 6000.00,
                "transaction_count": 3,
                "avg_per_transaction": 2000.00
            },
            ...
        ]
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                COALESCE(c.name, 'Uncategorized') as category,
                SUM(ABS(t.amount)) as amount,
                COUNT(t.id) as transaction_count,
                AVG(ABS(t.amount)) as avg_per_transaction
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.amount < 0 AND (c.type IS NULL OR c.type != 'transfer')
        """
        params = []
        
        if account_id:
            query += " AND t.account_id = ?"
            params.append(account_id)
        
        if start_date:
            query += " AND t.date >= ?"
            params.append(self._format_date(start_date))
        
        if end_date:
            query += " AND t.date <= ?"
            params.append(self._format_date(end_date))
        
        query += f"""
            GROUP BY c.name
            ORDER BY amount DESC
            LIMIT {limit}
        """
        
        cursor.execute(query, params)
        results = []
        
        for row in cursor.fetchall():
            amount = float(row['amount']) if row['amount'] else 0.0
            avg = float(row['avg_per_transaction']) if row['avg_per_transaction'] else 0.0
            results.append({
                'category': row['category'],
                'amount': round(amount, 2),
                'transaction_count': row['transaction_count'],
                'avg_per_transaction': round(avg, 2)
            })
        
        conn.close()
        return results

