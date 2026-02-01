import bcrypt
from app.database.db_connection import get_db_connection

# The user you want to make an admin
username = "admin"
password = "admin123"

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

with get_db_connection() as conn:
    cursor = conn.cursor()
    
    # Check if the user exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
        # Update existing user to be an admin and reset password
        cursor.execute(
            "UPDATE users SET role = 'admin', password = ? WHERE username = ?",
            (hashed, username)
        )
        print(f"✅ User '{username}' has been promoted to ADMIN.")
    else:
        # Create them from scratch if they don't exist
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, 'admin')",
            (username, "admin_final@example.com", hashed)
        )
        print(f"✅ New Admin user '{username}' created.")
    
    conn.commit()