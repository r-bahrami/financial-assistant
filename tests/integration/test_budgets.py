"""Integration tests for budget charts."""

import calendar
import sqlite3
from datetime import date

import pytest


def seed_budget_data(db_path: str):
    """Seed the test database with budget and transaction data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Account
    cursor.execute(
        """
        INSERT INTO accounts (name, type, institution)
        VALUES ('Primary Checking', 'checking', 'Test Bank')
        """
    )
    account_id = cursor.lastrowid

    # Categories
    cursor.execute(
        "INSERT INTO categories (name, parent_id, level, type) VALUES ('Groceries', NULL, 1, 'expense')"
    )
    groceries_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO categories (name, parent_id, level, type) VALUES ('Rent', NULL, 1, 'expense')"
    )
    rent_id = cursor.lastrowid

    # Current month boundaries
    today = date.today()
    start = date(today.year, today.month, 1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    end = date(today.year, today.month, last_day)

    # Budgets
    cursor.execute(
        """
        INSERT INTO budgets (category_id, amount, period_type, start_date, end_date, alert_threshold)
        VALUES (?, ?, 'monthly', ?, ?, 80)
        """,
        (groceries_id, 500.0, start.isoformat(), end.isoformat()),
    )
    cursor.execute(
        """
        INSERT INTO budgets (category_id, amount, period_type, start_date, end_date, alert_threshold)
        VALUES (?, ?, 'monthly', ?, ?, 80)
        """,
        (rent_id, 1000.0, start.isoformat(), end.isoformat()),
    )

    # Transactions (actual spending)
    cursor.execute(
        """
        INSERT INTO transactions (account_id, date, description, amount, category_id, notes, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (account_id, start.isoformat(), 'Groceries Spending', -350.0, groceries_id),
    )
    cursor.execute(
        """
        INSERT INTO transactions (account_id, date, description, amount, category_id, notes, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (account_id, (start.replace(day=10)).isoformat(), 'Rent Payment', -1100.0, rent_id),
    )

    conn.commit()
    conn.close()


def test_budget_category_chart_returns_data(client):
    seed_budget_data(client.application.config['DATABASE'])

    response = client.get('/budgets/api/charts/category')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert data['labels']

    # Ensure both categories are represented with expected values
    labels = data['labels']
    assert 'Groceries' in labels
    assert 'Rent' in labels

    groceries_index = labels.index('Groceries')
    rent_index = labels.index('Rent')

    assert pytest.approx(data['budgeted'][groceries_index], rel=1e-3) == 500.0
    assert pytest.approx(data['actual'][groceries_index], rel=1e-3) == 350.0
    assert data['statuses'][groceries_index] == 'good'

    assert pytest.approx(data['budgeted'][rent_index], rel=1e-3) == 1000.0
    assert pytest.approx(data['actual'][rent_index], rel=1e-3) == 1100.0
    assert data['statuses'][rent_index] == 'over'


def test_budget_trend_chart_includes_current_month(client):
    seed_budget_data(client.application.config['DATABASE'])

    response = client.get('/budgets/api/charts/trend?months=6')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert len(data['labels']) == 6
    assert len(data['budgeted']) == 6
    assert len(data['actual']) == 6

    # Latest month should reflect seeded totals
    latest_budgeted = data['budgeted'][-1]
    latest_actual = data['actual'][-1]
    assert pytest.approx(latest_budgeted, rel=1e-3) == 1500.0
    assert pytest.approx(latest_actual, rel=1e-3) == 1450.0

