"""
Pytest configuration and shared fixtures for Financial Assistant tests.
"""

import pytest
import os
import sys
import sqlite3
import tempfile

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from app import create_app

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # Initialize test database
    init_test_database(db_path)
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

def init_test_database(db_path):
    """Initialize a test database with schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create Accounts table
    cursor.execute("""
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('checking', 'savings', 'credit')),
            institution TEXT,
            initial_balance REAL DEFAULT 0,
            reference_date DATE,
            current_balance REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create Categories table
    cursor.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 3),
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE,
            UNIQUE(name, parent_id)
        );
    """)
    
    # Create Transactions table
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            date DATE NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            notes TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );
    """)

    # Create Transaction Notes table
    cursor.execute("""
        CREATE TABLE transaction_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL UNIQUE,
            note TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
        );
    """)

    # Create Tags table
    cursor.execute("""
        CREATE TABLE tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#667eea',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Create Transaction-Tags junction table
    cursor.execute("""
        CREATE TABLE transaction_tags (
            transaction_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (transaction_id, tag_id),
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
    """)

    # Useful indexes
    cursor.execute("CREATE INDEX idx_transactions_account ON transactions(account_id);")
    cursor.execute("CREATE INDEX idx_transactions_date ON transactions(date);")
    cursor.execute("CREATE INDEX idx_transaction_tags_transaction ON transaction_tags(transaction_id);")
    
    # Create Categorization Rules table
    cursor.execute("""
        CREATE TABLE categorization_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            priority INTEGER DEFAULT 0,
            match_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
            UNIQUE(pattern)
        );
    """)
    
    conn.commit()
    conn.close()

@pytest.fixture
def sample_account(app):
    """Create a sample account for testing."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO accounts (name, type, institution)
        VALUES ('Test Checking', 'checking', 'Test Bank')
    """)
    account_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return account_id

@pytest.fixture
def sample_category(app):
    """Create a sample category for testing."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO categories (name, parent_id, level, type)
        VALUES ('Test Category', NULL, 1, 'expense')
    """)
    category_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return category_id

