from branch_report import flag_large_withdrawals, format_kwd


def test_amount_above_threshold_is_flagged():
    data = [{"amount_kwd": 15000}]
    assert flag_large_withdrawals(data) == data


def test_amount_below_threshold_is_not_flagged():
    data = [{"amount_kwd": 9999.999}]
    assert flag_large_withdrawals(data) == []


def test_amount_exactly_at_threshold_is_flagged():
    data = [{"amount_kwd": 10000}]
    assert flag_large_withdrawals(data) == data


def test_custom_threshold_boundary_is_flagged():
    data = [{"amount_kwd": 500}]
    assert flag_large_withdrawals(data, threshold=500) == data


def test_format_kwd_uses_three_decimals():
    assert format_kwd(10000) == "10,000.000 KWD"


def test_format_kwd_negative_amount():
    assert format_kwd(-1500) == "-1,500.000 KWD"


def test_empty_list_returns_empty_list():
    assert flag_large_withdrawals([]) == []


import sqlite3
from branch_report import fetch_withdrawals


def test_join_does_not_duplicate_withdrawals(tmp_path):
    # tmp_path is a pytest-provided temporary folder, deleted afterwards
    db = tmp_path / "test.db"
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE branches (branch_id INTEGER, name TEXT);
        CREATE TABLE accounts (account_id INTEGER, customer_name TEXT, branch_id INTEGER);
        CREATE TABLE transactions (txn_id INTEGER, account_id INTEGER, txn_date TEXT,
                                   amount_kwd REAL, channel TEXT, kind TEXT);
        -- Two rows share branch_id 1: this is what causes fan-out
        INSERT INTO branches VALUES (1, 'Salmiya'), (1, 'Salmiya (old)');
        INSERT INTO accounts VALUES (100, 'Test Customer', 1);
        INSERT INTO transactions VALUES (1, 100, '2026-09-26', 12000, 'teller', 'withdrawal');
    """)
    con.commit()
    con.close()

    rows = fetch_withdrawals(str(db))
    txn_ids = [r["txn_id"] for r in rows]
    # A set removes duplicates, so the lengths only match if every txn_id is unique
    assert len(txn_ids) == len(set(txn_ids))
