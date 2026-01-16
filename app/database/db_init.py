from app.database.db_connection import create_database

def init_db():
    create_database()
    print("✅ Database initialized successfully")

if __name__ == "__main__":
    init_db()
