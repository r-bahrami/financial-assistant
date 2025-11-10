"""
Financial Assistant - Flask Application

A local web-based financial analysis application for tracking,
categorizing, and analyzing bank and credit card transactions.
"""

import os
import sys
from flask import Flask, render_template
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Application factory pattern
def create_app():
    """Create and configure the Flask application."""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DATABASE'] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'financial_assistant.db'
    )
    
    # Custom Jinja filters
    @app.template_filter('format_currency')
    def format_currency(value):
        """Format number as currency with $###,###.## format."""
        try:
            return f"${abs(float(value)):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"
    
    # Register routes
    register_routes(app)
    
    return app

def register_routes(app):
    """Register all application routes."""
    
    # Import blueprints
    from routes.accounts import accounts_bp
    from routes.import_routes import import_bp
    from routes.transactions import transactions_bp
    from routes.admin import admin_bp
    from routes.categories import categories_bp
    from routes.reports import reports_bp
    from routes.budgets import budgets_bp
    from routes.recurring import recurring_bp
    from routes.dashboard import dashboard_bp
    from routes.tags import tags_bp
    from routes.goals import goals_bp
    
    # Register blueprints
    app.register_blueprint(accounts_bp)
    app.register_blueprint(import_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(budgets_bp)
    app.register_blueprint(recurring_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(goals_bp)
    
    @app.route('/')
    def index():
        """Home page route."""
        return render_template('index.html', 
                             app_name='Financial Assistant',
                             current_year=datetime.now().year)
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return {'status': 'ok', 'message': 'Financial Assistant is running'}
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        return render_template('500.html'), 500

def main():
    """Run the Flask application."""
    
    # Check if database exists
    app = create_app()
    if not os.path.exists(app.config['DATABASE']):
        print("⚠️  Database not found!")
        print(f"Please run: python src/init_db.py")
        sys.exit(1)
    
    # Run the application
    print("=" * 60)
    print("Financial Assistant - Starting...")
    print("=" * 60)
    print(f"Server running at: http://localhost:5001")
    print(f"Database location: {app.config['DATABASE']}")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print("")
    print("NOTE: Using port 5001 because port 5000 is used by macOS AirPlay")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()

