from app.database.db_connection import get_db_connection


def create_user(name, email, password, role="user"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (name, email, password, role))

    conn.commit()
    conn.close()


def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY name
    """)

    users = cursor.fetchall()
    conn.close()
    return users


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, role, created_at
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, password, role
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()
    return user


def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()
