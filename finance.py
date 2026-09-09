from database import get_connection
from datetime import datetime

def add_transaction(user_id, t_type, category, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, t_type, category, amount, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, type, category, amount, date FROM transactions WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchall()
    conn.close()
    return data

def get_summary(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='income'",
        (user_id,)
    )
    income = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='expense'",
        (user_id,)
    )
    expense = cursor.fetchone()[0] or 0

    conn.close()
    return income, expense, income - expense
def delete_transaction(transaction_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id=? AND user_id=?",
        (transaction_id, user_id)
    )

    conn.commit()
    conn.close()

