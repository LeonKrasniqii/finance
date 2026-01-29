import bcrypt
from app.database.db_connection import get_db_connection

# Admin credentials
username = "admin"
email = "admin@example.com"
password = "admin123"

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, 'admin')
        """,
        (username, email, hashed)
    )
    conn.commit()

print("✅ Admin user created")  # <-- make sure this line exists
