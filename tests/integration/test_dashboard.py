from datetime import date, timedelta


def seed_dashboard_data(app, sample_account, sample_category):
    db_path = app.config["DATABASE"]
    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    today = date.today()
    within_range = today - timedelta(days=5)

    # Insert income transaction
    cursor.execute(
        """
        INSERT INTO transactions (account_id, date, description, amount, category_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (sample_account, within_range.isoformat(), "Salary", 4000.0, sample_category),
    )

    # Insert expense transactions
    cursor.execute(
        """
        INSERT INTO transactions (account_id, date, description, amount, category_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (sample_account, within_range.isoformat(), "Rent", -1500.0, sample_category),
    )
    cursor.execute(
        """
        INSERT INTO transactions (account_id, date, description, amount, category_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (sample_account, within_range.isoformat(), "Groceries", -300.0, sample_category),
    )

    # Update account balance
    cursor.execute(
        "UPDATE accounts SET current_balance = ? WHERE id = ?",
        (2500.0, sample_account),
    )

    # Add a budget to increase health score
    cursor.execute(
        """
        INSERT INTO budgets (category_id, amount, period_type, start_date, end_date, alert_threshold, created_at, updated_at)
        VALUES (?, ?, 'monthly', ?, ?, 80, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (
            sample_category,
            2000.0,
            today.replace(day=1).isoformat(),
            today.isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def test_dashboard_health_endpoint(client, app, sample_account, sample_category):
    seed_dashboard_data(app, sample_account, sample_category)

    response = client.get("/dashboard/api/health")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["success"] is True

    health = payload["health"]
    assert health["income_30d"] == 4000.0
    assert health["expenses_30d"] == 1800.0
    assert health["net_income"] == 2200.0
    assert health["budget_count"] == 1
    assert health["total_balance"] == 2500.0
    assert isinstance(health["health_score"], (int, float))
    assert health["health_score"] >= 0
    assert health["top_categories"]


def test_dashboard_page_renders(client):
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert b"Financial Health Dashboard" in response.data

