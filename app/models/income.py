from app.database.db_connection import get_db_connection


def create_income(user_id, amount, source, income_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO income (user_id, amount, source, income_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, source, income_date))

    conn.commit()
    conn.close()


def get_income_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            source,
            income_date,
            created_at
        FROM income
        WHERE user_id = ?
        ORDER BY income_date DESC
    """, (user_id,))

    income = cursor.fetchall()
    conn.close()
    return income


def get_income_by_id(income_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            source,
            income_date
        FROM income
        WHERE id = ? AND user_id = ?
    """, (income_id, user_id))

    income = cursor.fetchone()
    conn.close()
    return income


def delete_income(income_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM income
        WHERE id = ? AND user_id = ?
    """, (income_id, user_id))

    conn.commit()
    conn.close()
