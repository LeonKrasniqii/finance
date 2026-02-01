from app.database import SessionLocal

def test_db_connection():
    db = SessionLocal()
    assert db is not None
    db.close()
#nuk nevoiten