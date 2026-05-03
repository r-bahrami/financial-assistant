"""Savings Goal Model"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Goal:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_all(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT g.*, c.name as category_name
                FROM savings_goals g
                LEFT JOIN categories c ON g.category_id = c.id
                ORDER BY g.target_date ASC
            """)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_by_id(self, goal_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT g.*, c.name as category_name
                FROM savings_goals g
                LEFT JOIN categories c ON g.category_id = c.id
                WHERE g.id = ?
            """, (goal_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def create(self, name: str, target_amount: float, target_date: Optional[str],
               category_id: Optional[int] = None, current_amount: float = 0.0,
               status: str = 'active') -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO savings_goals (name, target_amount, current_amount, target_date, category_id, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                target_amount,
                current_amount,
                target_date,
                category_id,
                status,
                datetime.now(),
                datetime.now()
            ))
            
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def update(self, goal_id: int, updates: Dict) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            fields = []
            params = []
            
            for field in ['name', 'target_amount', 'current_amount', 'target_date', 'category_id', 'status']:
                if field in updates:
                    fields.append(f"{field} = ?")
                    params.append(updates[field])
            
            if not fields:
                return True
            
            fields.append("updated_at = ?")
            params.append(datetime.now())
            params.append(goal_id)
            
            cursor.execute(f"UPDATE savings_goals SET {', '.join(fields)} WHERE id = ?", params)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete(self, goal_id: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM savings_goals WHERE id = ?", (goal_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
