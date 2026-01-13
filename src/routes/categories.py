"""
Category routes for category management.
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from models.category import Category
from models.transaction import Transaction
from services.categorization_engine import CategorizationEngine

# Create blueprint
categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
def categories_page():
    """Render the categories overview page."""
    return render_template('categories.html')


@categories_bp.route('/manage')
def category_management_page():
    """Render the category management page."""
    return render_template('category_management.html')


@categories_bp.route('/api/all', methods=['GET'])
def get_all_categories():
    """
    Get all categories with transaction counts.
    
    Returns:
        JSON list of categories with usage stats
    """
    try:
        import sqlite3
        category_model = Category(current_app.config['DATABASE'])
        categories = category_model.get_all()
        
        # Get transaction count for each category
        conn = sqlite3.connect(current_app.config['DATABASE'])
        cursor = conn.cursor()
        
        for cat in categories:
            cursor.execute("""
                SELECT COUNT(*) FROM transactions WHERE category_id = ?
            """, (cat['id'],))
            cat['transaction_count'] = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'categories': categories,
            'count': len(categories)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/hierarchy', methods=['GET'])
def get_category_hierarchy():
    """
    Get categories organized as hierarchy.
    
    Returns:
        JSON with income and expense category trees
    """
    try:
        category_model = Category(current_app.config['DATABASE'])
        hierarchy = category_model.get_hierarchy()
        
        return jsonify({
            'success': True,
            'hierarchy': hierarchy
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get a specific category.
    
    Args:
        category_id: Category ID
    
    Returns:
        JSON category details or 404
    """
    try:
        category_model = Category(current_app.config['DATABASE'])
        category = category_model.get_by_id(category_id)
        
        if not category:
            return jsonify({'success': False, 'error': 'Category not found'}), 404
        
        return jsonify({
            'success': True,
            'category': category
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/create', methods=['POST'])
def create_category():
    """
    Create a new category.
    
    Request JSON:
        {
            "name": str,
            "level": int (1-3),
            "type": "income" | "expense" | "transfer",
            "parent_id": int (optional)
        }
    
    Returns:
        JSON with new category ID
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        name = data.get('name')
        level = data.get('level')
        category_type = data.get('type')
        parent_id = data.get('parent_id')
        
        if not all([name, level, category_type]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        category_model = Category(current_app.config['DATABASE'])
        category_id = category_model.create(name, level, category_type, parent_id)
        
        return jsonify({
            'success': True,
            'message': f'Category "{name}" created successfully',
            'category_id': category_id
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Update a category.
    
    Request JSON:
        {
            "name": str (optional),
            "parent_id": int (optional)
        }
    
    Returns:
        JSON success message
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        name = data.get('name')
        parent_id = data.get('parent_id')
        
        category_model = Category(current_app.config['DATABASE'])
        success = category_model.update(category_id, name=name, parent_id=parent_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Category not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Category updated successfully'
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category."""
    try:
        category_model = Category(current_app.config['DATABASE'])
        success = category_model.delete(category_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Category not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/rules/create', methods=['POST'])
def create_rule():
    """
    Create a new categorization rule.
    
    Request JSON:
        {
            "pattern": str,
            "category_id": int,
            "priority": int (0-100)
        }
    
    Returns:
        JSON with new rule ID
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        pattern = data.get('pattern', '').strip().upper()
        category_id = data.get('category_id')
        priority = data.get('priority', 50)
        
        if not all([pattern, category_id]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        engine = CategorizationEngine(current_app.config['DATABASE'])
        rule_id = engine.create_rule(pattern, category_id, priority)
        
        return jsonify({
            'success': True,
            'message': f'Rule "{pattern}" created successfully',
            'rule_id': rule_id
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/rules/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    """
    Update a categorization rule.
    
    Request JSON:
        {
            "pattern": str (optional),
            "category_id": int (optional),
            "priority": int (optional, 0-100)
        }
    
    Returns:
        JSON success message
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        pattern = data.get('pattern')
        category_id = data.get('category_id')
        priority = data.get('priority')
        
        engine = CategorizationEngine(current_app.config['DATABASE'])
        success = engine.update_rule(rule_id, pattern=pattern, category_id=category_id, priority=priority)
        
        if not success:
            return jsonify({'success': False, 'error': 'Rule not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Rule updated successfully'
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    """Delete a categorization rule."""
    try:
        import sqlite3
        conn = sqlite3.connect(current_app.config['DATABASE'])
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM categorization_rules WHERE id = ?", (rule_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        if not deleted:
            return jsonify({'success': False, 'error': 'Rule not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Rule deleted successfully'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/categorize/<int:transaction_id>', methods=['PUT'])
def categorize_transaction(transaction_id):
    """
    Manually categorize a transaction.
    
    Args:
        transaction_id: Transaction ID
    
    Request JSON:
        {
            "category_id": int,
            "learn": bool (optional, default: false)
        }
    
    Returns:
        JSON success message
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        category_id = data.get('category_id')
        learn = data.get('learn', False)
        
        # Get transaction
        transaction = Transaction.get_by_id(transaction_id)
        
        if not transaction:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        # Update transaction category
        conn = current_app.config['DATABASE']
        import sqlite3
        db_conn = sqlite3.connect(conn)
        cursor = db_conn.cursor()
        
        cursor.execute("""
            UPDATE transactions
            SET category_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (category_id, transaction_id))
        
        db_conn.commit()
        db_conn.close()
        
        # Learn from categorization if requested
        rule_id = None
        if learn and category_id:
            engine = CategorizationEngine(current_app.config['DATABASE'])
            rule_id = engine.learn_from_categorization(
                transaction['description'],
                category_id
            )
        
        response = {
            'success': True,
            'message': 'Transaction categorized successfully'
        }
        
        if rule_id:
            response['rule_created'] = True
            response['rule_id'] = rule_id
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/bulk-categorize', methods=['POST'])
def bulk_categorize():
    """
    Categorize multiple transactions at once.
    
    Request JSON:
        {
            "transaction_ids": [int, int, ...],
            "category_id": int,
            "learn": bool (optional)
        }
    
    Returns:
        JSON with count of updated transactions
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        transaction_ids = data.get('transaction_ids', [])
        category_id = data.get('category_id')
        learn = data.get('learn', False)
        
        if not transaction_ids:
            return jsonify({'success': False, 'error': 'No transaction IDs provided'}), 400
        
        # Update all transactions
        import sqlite3
        conn = sqlite3.connect(current_app.config['DATABASE'])
        cursor = conn.cursor()
        
        placeholders = ','.join(['?'] * len(transaction_ids))
        cursor.execute(f"""
            UPDATE transactions
            SET category_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id IN ({placeholders})
        """, [category_id] + transaction_ids)
        
        updated_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        # Learn from first transaction if requested
        rule_id = None
        if learn and category_id and transaction_ids:
            first_transaction = Transaction.get_by_id(transaction_ids[0])
            if first_transaction:
                engine = CategorizationEngine(current_app.config['DATABASE'])
                rule_id = engine.learn_from_categorization(
                    first_transaction['description'],
                    category_id
                )
        
        response = {
            'success': True,
            'message': f'Successfully categorized {updated_count} transactions',
            'count': updated_count
        }
        
        if rule_id:
            response['rule_created'] = True
            response['rule_id'] = rule_id
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all categorization rules."""
    try:
        import sqlite3
        conn = sqlite3.connect(current_app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.*, c.name as category_name, c.type as category_type
            FROM categorization_rules r
            JOIN categories c ON r.category_id = c.id
            ORDER BY r.priority DESC, r.match_count DESC
            LIMIT 100
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return jsonify({'success': True, 'rules': [dict(row) for row in rows], 'count': len(rows)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/stats', methods=['GET'])
def get_category_stats():
    """Get categorization statistics."""
    try:
        import sqlite3
        conn = sqlite3.connect(current_app.config['DATABASE'])
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM categories")
        total_categories = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM categorization_rules")
        total_rules = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE category_id IS NOT NULL")
        categorized = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE category_id IS NULL")
        uncategorized = cursor.fetchone()[0]
        
        total_transactions = categorized + uncategorized
        rate = (categorized / total_transactions * 100) if total_transactions > 0 else 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_categories': total_categories,
                'total_rules': total_rules,
                'categorized': categorized,
                'uncategorized': uncategorized,
                'total_transactions': total_transactions,
                'categorization_rate': round(rate, 1)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@categories_bp.route('/api/recategorize-all', methods=['POST'])
def recategorize_all_transactions():
    """
    Apply categorization rules to transactions.
    
    Query params:
        mode: 'soft' (uncategorized only, default) or 'hard' (ALL transactions, override existing)
    """
    try:
        import sqlite3
        
        mode = request.args.get('mode', 'soft')
        
        conn = sqlite3.connect(current_app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get transactions based on mode
        if mode == 'hard':
            # HARD mode: Get ALL transactions (override existing categories)
            cursor.execute("""
                SELECT id, description, amount, category_id
                FROM transactions
                ORDER BY date DESC
            """)
        else:
            # SOFT mode (default): Only uncategorized transactions
            cursor.execute("""
                SELECT id, description, amount, category_id
                FROM transactions
                WHERE category_id IS NULL
                ORDER BY date DESC
            """)
        
        transactions = cursor.fetchall()
        total_transactions = len(transactions)
        
        if total_transactions == 0:
            conn.close()
            message = 'All transactions are already categorized!' if mode == 'soft' else 'No transactions found!'
            return jsonify({
                'success': True,
                'total': 0,
                'categorized': 0,
                'success_rate': 100.0,
                'message': message
            })
        
        # Initialize categorization engine
        engine = CategorizationEngine(current_app.config['DATABASE'])
        
        categorized_count = 0
        
        for txn in transactions:
            # Create transaction dict
            transaction = {
                'id': txn['id'],
                'description': txn['description'],
                'amount': txn['amount']
            }
            
            # Try to categorize
            result = engine.categorize_transaction(transaction)
            
            if result and result['category_id']:
                category_id = result['category_id']
                
                # Update transaction
                cursor.execute("""
                    UPDATE transactions 
                    SET category_id = ?
                    WHERE id = ?
                """, (category_id, txn['id']))
                
                categorized_count += 1
        
        conn.commit()
        conn.close()
        
        success_rate = (categorized_count / total_transactions * 100) if total_transactions > 0 else 0
        
        return jsonify({
            'success': True,
            'total': total_transactions,
            'categorized': categorized_count,
            'success_rate': round(success_rate, 1),
            'mode': mode
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
