import math

import pytest

from routes.dashboard import calculate_health_score


@pytest.mark.parametrize(
    "savings_rate,total_balance,total_budgets,net_income,expected",
    [
        (25, 6000, 2, 1200, 100),  # max thresholds hit
        (15, 3000, 0, -100, 50),  # mid-tier savings, balance, no budgets, negative net income
        (5, 0, 0, -500, 20),  # low savings rate but positive, no balance/budgets
        (0, 0, 0, 0, 0),  # baseline
    ],
)
def test_calculate_health_score_various_inputs(
    savings_rate, total_balance, total_budgets, net_income, expected
):
    score = calculate_health_score(savings_rate, total_balance, total_budgets, net_income)
    assert score == expected


def test_calculate_health_score_clamped_to_100():
    # Even with exaggerated inputs the score should never exceed 100
    score = calculate_health_score(100, 100_000, 10, 50_000)
    assert score == 100

