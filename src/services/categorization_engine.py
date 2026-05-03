"""
Categorization Engine for automatic transaction categorization.

Uses pattern-based rules to automatically categorize transactions.
"""

import sqlite3
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class CategorizationEngine:
    """
    Service for automatically categorizing transactions based on patterns.
    """
    
    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.90
    MEDIUM_CONFIDENCE_THRESHOLD = 0.70
    LOW_CONFIDENCE_THRESHOLD = 0.50
    
    def __init__(self, db_path: str):
        """
        Initialize the categorization engine.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def categorize_transaction(self, transaction: Dict) -> Dict:
        """
        Categorize a single transaction.
        
        Args:
            transaction: Dictionary with 'description' and optionally 'amount'
        
        Returns:
            Dictionary with:
                - category_id: Matched category ID (or None)
                - confidence: Confidence score (0.0 to 1.0)
                - rule_id: Matched rule ID (or None)
                - category_name: Full category path
        """
        description = transaction.get('description', '').strip()
        amount = transaction.get('amount', 0)
        
        if not description:
            return self._no_match_result()
        
        # Get all rules sorted by priority
        rules = self._get_all_rules()
        
        if not rules:
            return self._no_match_result()
        
        # Find best matching rule
        best_match = None
        best_confidence = 0.0
        
        for rule in rules:
            confidence = self._calculate_match_confidence(description, rule['pattern'])
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = rule
        
        # Return result if confidence meets threshold
        if best_match and best_confidence >= self.LOW_CONFIDENCE_THRESHOLD:
            category_path = self._get_category_path(best_match['category_id'])
            
            return {
                'category_id': best_match['category_id'],
                'confidence': best_confidence,
                'rule_id': best_match['id'],
                'category_name': category_path
            }
        
        return self._no_match_result()
    
    def categorize_transactions_bulk(self, transactions: List[Dict]) -> List[Dict]:
        """
        Categorize multiple transactions.
        
        Args:
            transactions: List of transaction dictionaries
        
        Returns:
            List of categorization results
        """
        return [self.categorize_transaction(txn) for txn in transactions]
    
    def create_rule(self, pattern: str, category_id: int, 
                   priority: int = 0) -> int:
        """
        Create a new categorization rule.
        
        Args:
            pattern: Regular expression pattern to match
            category_id: Category to assign
            priority: Rule priority (higher = checked first)
        
        Returns:
            Rule ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO categorization_rules (pattern, category_id, priority)
                VALUES (?, ?, ?)
            """, (pattern.upper(), category_id, priority))
            
            rule_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return rule_id
        
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Rule with pattern '{pattern}' already exists")
    
    def update_rule(self, rule_id: int, pattern: Optional[str] = None,
                    category_id: Optional[int] = None, priority: Optional[int] = None) -> bool:
        """
        Update a categorization rule.
        
        Args:
            rule_id: Rule ID
            pattern: Optional new pattern
            category_id: Optional new category ID
            priority: Optional new priority
        
        Returns:
            True if updated, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build update query
        updates = []
        params = []
        
        if pattern is not None:
            updates.append("pattern = ?")
            params.append(pattern.upper().strip())
        
        if category_id is not None:
            updates.append("category_id = ?")
            params.append(category_id)
        
        if priority is not None:
            updates.append("priority = ?")
            params.append(priority)
        
        if not updates:
            conn.close()
            return True  # Nothing to update
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(rule_id)
        
        query = f"UPDATE categorization_rules SET {', '.join(updates)} WHERE id = ?"
        
        try:
            cursor.execute(query, params)
            updated = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return updated
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Rule with pattern '{pattern}' already exists")
    
    def update_rule_match_count(self, rule_id: int):
        """
        Increment the match count for a rule.
        
        Args:
            rule_id: Rule ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE categorization_rules 
            SET match_count = match_count + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (rule_id,))
        
        conn.commit()
        conn.close()
    
    def learn_from_categorization(self, description: str, category_id: int) -> Optional[int]:
        """
        Learn from user categorization by creating/updating rules.
        
        Args:
            description: Transaction description
            category_id: Category assigned by user
        
        Returns:
            Rule ID (new or existing)
        """
        # Extract meaningful pattern from description
        pattern = self._extract_pattern(description)
        
        if not pattern:
            return None
        
        # Check if rule already exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, category_id FROM categorization_rules WHERE pattern = ?
        """, (pattern,))
        
        row = cursor.fetchone()
        
        if row:
            existing_rule_id, existing_category_id = row
            
            # If categories match, just increment count
            if existing_category_id == category_id:
                conn.close()
                self.update_rule_match_count(existing_rule_id)
                return existing_rule_id
            
            # If different category, update the rule
            cursor.execute("""
                UPDATE categorization_rules
                SET category_id = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (category_id, existing_rule_id))
            
            conn.commit()
            conn.close()
            
            return existing_rule_id
        
        conn.close()
        
        # Create new rule with user priority
        return self.create_rule(pattern, category_id, priority=100)
    
    def _get_all_rules(self) -> List[Dict]:
        """Get all categorization rules, sorted by priority."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.*,
                   c.name as category_name
            FROM categorization_rules r
            JOIN categories c ON r.category_id = c.id
            ORDER BY r.priority DESC, r.match_count DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def _calculate_match_confidence(self, description: str, pattern: str) -> float:
        """
        Calculate confidence that pattern matches description.
        
        Args:
            description: Transaction description
            pattern: Pattern to match (can include | for OR)
        
        Returns:
            Confidence score from 0.0 to 1.0
        """
        description_upper = description.upper()
        pattern_upper = pattern.upper()
        
        # Check for exact match
        if pattern_upper in description_upper:
            # Calculate match strength based on length
            pattern_length = len(pattern_upper)
            description_length = len(description_upper)
            
            # If pattern is most of the description, high confidence
            if pattern_length >= description_length * 0.7:
                return 1.0
            elif pattern_length >= description_length * 0.5:
                return 0.95
            elif pattern_length >= description_length * 0.3:
                return 0.90
            else:
                return 0.85
        
        # Check for partial match with OR patterns (e.g., "COSTCO|WALMART")
        if '|' in pattern_upper:
            patterns = [p.strip() for p in pattern_upper.split('|')]
            for p in patterns:
                if p in description_upper:
                    # Found one of the OR patterns
                    return 0.85
        
        # Check for word boundaries (whole word match)
        pattern_words = pattern_upper.split()
        description_words = description_upper.split()
        
        matches = sum(1 for pw in pattern_words if pw in description_words)
        if matches > 0 and pattern_words:
            return 0.70 + (matches / len(pattern_words)) * 0.15
        
        return 0.0
    
    def _extract_pattern(self, description: str) -> Optional[str]:
        """
        Extract a meaningful pattern from a transaction description.
        
        Args:
            description: Transaction description
        
        Returns:
            Extracted pattern or None
        """
        # Clean description
        description = description.upper().strip()
        
        # Remove common noise words
        noise_words = ['THE', 'AND', 'OR', 'OF', 'AT', 'IN', 'ON', 'FOR']
        
        # Remove numbers, hashes, special characters
        cleaned = re.sub(r'[#*\d]+', '', description)
        cleaned = ' '.join(cleaned.split())  # Normalize whitespace
        
        # Extract first significant word(s)
        words = cleaned.split()
        significant_words = [w for w in words if w not in noise_words and len(w) > 2]
        
        if not significant_words:
            return None
        
        # Use first 1-2 significant words
        if len(significant_words) >= 2:
            return ' '.join(significant_words[:2])
        else:
            return significant_words[0]
    
    def _get_category_path(self, category_id: int) -> str:
        """Get full category path."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        path = []
        current_id = category_id
        
        while current_id:
            cursor.execute("SELECT id, name, parent_id FROM categories WHERE id = ?", (current_id,))
            row = cursor.fetchone()
            
            if not row:
                break
            
            path.insert(0, row['name'])
            current_id = row['parent_id']
        
        conn.close()
        
        return ' → '.join(path) if path else 'Uncategorized'
    
    def _no_match_result(self) -> Dict:
        """Return result for no match."""
        return {
            'category_id': None,
            'confidence': 0.0,
            'rule_id': None,
            'category_name': 'Uncategorized'
        }

