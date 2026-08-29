import sqlite3
import os


DATABASE_NAME = "database/expenses.db"


def get_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DATABASE_NAME, check_same_thread=False)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(date, category, amount, payment_method, description):
    conn = get_connection()

    conn.execute("""
        INSERT INTO expenses
        (date, category, amount, payment_method, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        str(date),
        category,
        amount,
        payment_method,
        description
    ))

    conn.commit()
    conn.close()


def get_expenses():
    conn = get_connection()

    query = """
        SELECT
            id,
            date,
            category,
            amount,
            payment_method,
            description
        FROM expenses
        ORDER BY date DESC
    """

    df = __import__("pandas").read_sql_query(query, conn)

    conn.close()

    return df


def delete_expense(expense_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()


def set_budget(month, amount):
    conn = get_connection()

    conn.execute("""
        INSERT INTO budgets (month, amount)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount = excluded.amount
    """, (
        month,
        amount
    ))

    conn.commit()
    conn.close()


def get_budget(month):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM budgets WHERE month = ?",
        (month,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0