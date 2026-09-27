"""NBK Branch Daily Report.

Reads the branch database, finds yesterday's large cash withdrawals, and prints a
report a branch manager could act on.

All data in this file is fictional and generated for training.
"""
import sqlite3

DB_PATH = "nbk_demo.db"
FLAG_THRESHOLD_KWD = 10000

QUERY = """
SELECT t.txn_id,
       a.customer_name,
       b.name AS branch,
       t.txn_date,
       t.amount_kwd,
       t.channel
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN branches b ON a.branch_id  = b.branch_id
WHERE t.kind = 'withdrawal'
ORDER BY t.amount_kwd DESC
"""


def format_kwd(amount):
    """Return a Kuwaiti dinar amount as text, with 3 decimal places and a separator."""
    return f"{amount:,.3f} KWD"


def flag_large_withdrawals(withdrawals, threshold=FLAG_THRESHOLD_KWD):
    """Return only the withdrawals at or above the threshold.

    withdrawals is a list of dictionaries. Each one needs an "amount_kwd" key.
    This function does not touch the database, which is what makes it testable.
    """
    flagged = []
    for w in withdrawals:
        if w["amount_kwd"] > threshold:
            flagged.append(w)
    return flagged


def fetch_withdrawals(db_path=DB_PATH):
    """Read every withdrawal out of the database as a list of dictionaries."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    rows = connection.execute(QUERY).fetchall()
    connection.close()
    return [dict(row) for row in rows]


def main():
    withdrawals = fetch_withdrawals()
    flagged = flag_large_withdrawals(withdrawals)

    print("NBK BRANCH DAILY REPORT")
    print("Withdrawals at or above " + format_kwd(FLAG_THRESHOLD_KWD))
    print("")

    if not flagged:
        print("No withdrawals to review today.")
        return

    for w in flagged:
        print(w["txn_date"] + "  " + w["branch"].ljust(12) + "  "
              + w["customer_name"].ljust(22) + format_kwd(w["amount_kwd"]).rjust(16)
              + "  " + w["channel"])

    print("")
    print("Flagged " + str(len(flagged)) + " of " + str(len(withdrawals)) + " withdrawals.")


if __name__ == "__main__":
    main()