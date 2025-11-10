"""
Unit tests for Account model.
"""

import pytest
import tempfile
import os
from src.models.account import Account


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    
    # Initialize database with accounts table
    import sqlite3
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
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
        )
    """)
    
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
            FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE transaction_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL UNIQUE,
            note TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#667eea',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE transaction_tags (
            transaction_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (transaction_id, tag_id),
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    
    yield path
    
    os.close(fd)
    os.unlink(path)


def test_create_account(temp_db):
    """Test creating a new account."""
    account = Account(temp_db)
    account_id = account.create('Test Checking', 'checking', 'Test Bank')
    
    assert account_id > 0
    
    # Verify it was created
    created = account.get_by_id(account_id)
    assert created is not None
    assert created['name'] == 'Test Checking'
    assert created['type'] == 'checking'
    assert created['institution'] == 'Test Bank'


def test_create_account_without_institution(temp_db):
    """Test creating account without institution."""
    account = Account(temp_db)
    account_id = account.create('My Savings', 'savings')
    
    assert account_id > 0
    
    created = account.get_by_id(account_id)
    assert created['institution'] is None


def test_create_account_validates_name(temp_db):
    """Test that empty name is rejected."""
    account = Account(temp_db)
    
    with pytest.raises(ValueError, match="Account name is required"):
        account.create('', 'checking')
    
    with pytest.raises(ValueError, match="Account name is required"):
        account.create('   ', 'checking')


def test_create_account_validates_type(temp_db):
    """Test that invalid type is rejected."""
    account = Account(temp_db)
    
    with pytest.raises(ValueError, match="Account type must be"):
        account.create('Test Account', 'invalid_type')


def test_get_all_accounts_empty(temp_db):
    """Test getting all accounts when none exist."""
    account = Account(temp_db)
    accounts = account.get_all()
    
    assert accounts == []


def test_get_all_accounts(temp_db):
    """Test getting all accounts."""
    account = Account(temp_db)
    
    # Create multiple accounts
    account.create('Checking', 'checking', 'Bank A')
    account.create('Savings', 'savings', 'Bank B')
    account.create('Credit Card', 'credit', 'Bank C')
    
    accounts = account.get_all()
    
    assert len(accounts) == 3
    assert accounts[0]['name'] == 'Credit Card'  # Most recent first
    assert accounts[1]['name'] == 'Savings'
    assert accounts[2]['name'] == 'Checking'


def test_get_account_by_id(temp_db):
    """Test getting account by ID."""
    account = Account(temp_db)
    account_id = account.create('Test Account', 'checking')
    
    result = account.get_by_id(account_id)
    
    assert result is not None
    assert result['id'] == account_id
    assert result['name'] == 'Test Account'


def test_get_account_by_id_not_found(temp_db):
    """Test getting non-existent account."""
    account = Account(temp_db)
    result = account.get_by_id(99999)
    
    assert result is None


def test_update_account_name(temp_db):
    """Test updating account name."""
    account = Account(temp_db)
    account_id = account.create('Old Name', 'checking')
    
    success = account.update(account_id, name='New Name')
    
    assert success is True
    
    updated = account.get_by_id(account_id)
    assert updated['name'] == 'New Name'
    assert updated['type'] == 'checking'  # Unchanged


def test_update_account_type(temp_db):
    """Test updating account type."""
    account = Account(temp_db)
    account_id = account.create('My Account', 'checking')
    
    success = account.update(account_id, account_type='savings')
    
    assert success is True
    
    updated = account.get_by_id(account_id)
    assert updated['type'] == 'savings'


def test_update_account_institution(temp_db):
    """Test updating account institution."""
    account = Account(temp_db)
    account_id = account.create('Account', 'checking', 'Old Bank')
    
    success = account.update(account_id, institution='New Bank')
    
    assert success is True
    
    updated = account.get_by_id(account_id)
    assert updated['institution'] == 'New Bank'


def test_update_account_not_found(temp_db):
    """Test updating non-existent account."""
    account = Account(temp_db)
    success = account.update(99999, name='New Name')
    
    assert success is False


def test_update_account_validates_name(temp_db):
    """Test that update validates name."""
    account = Account(temp_db)
    account_id = account.create('Account', 'checking')
    
    with pytest.raises(ValueError, match="Account name cannot be empty"):
        account.update(account_id, name='')


def test_update_account_validates_type(temp_db):
    """Test that update validates type."""
    account = Account(temp_db)
    account_id = account.create('Account', 'checking')
    
    with pytest.raises(ValueError, match="Account type must be"):
        account.update(account_id, account_type='invalid')


def test_delete_account(temp_db):
    """Test deleting an account."""
    account = Account(temp_db)
    account_id = account.create('Account', 'checking')
    
    success = account.delete(account_id)
    
    assert success is True
    assert account.get_by_id(account_id) is None


def test_delete_account_not_found(temp_db):
    """Test deleting non-existent account."""
    account = Account(temp_db)
    success = account.delete(99999)
    
    assert success is False


def test_get_transaction_count_zero(temp_db):
    """Test transaction count for account with no transactions."""
    account = Account(temp_db)
    account_id = account.create('Account', 'checking')
    
    count = account.get_transaction_count(account_id)
    
    assert count == 0


def test_get_transaction_count(temp_db):
    """Test transaction count for account with transactions."""
    import sqlite3
    from datetime import date
    
    account = Account(temp_db)
    account_id = account.create('Account', 'checking')
    
    # Add some transactions
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    
    for i in range(3):
        cursor.execute("""
            INSERT INTO transactions (account_id, date, description, amount)
            VALUES (?, ?, ?, ?)
        """, (account_id, date.today(), f'Transaction {i}', 100.0))
    
    conn.commit()
    conn.close()
    
    count = account.get_transaction_count(account_id)
    
    assert count == 3

