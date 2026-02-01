from fastapi import APIRouter, Depends, HTTPException, Header
from app.routers.auth_routes import decode_access_token
from app.database.db_connection import get_db_connection

router = APIRouter(prefix="/admin", tags=["Admin"])

def verify_admin(authorization: str = Header(None)):
    if not authorization:
        # This matches the error you were seeing in Swagger
        raise HTTPException(status_code=401, detail="No token provided")
    
    # Cleans "Bearer " prefix if present before decoding
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    payload = decode_access_token(token)
    
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload

@router.get("/users")
def get_all_users(admin_data=Depends(verify_admin)):
    # FIXED: Instead of just a message, we now query the database
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Fetching all users from the users table
        cursor.execute("SELECT id, username, email, role FROM users")
        rows = cursor.fetchall()
        
        # Return the actual list of users
        return [
            {
                "id": r[0],
                "username": r[1],
                "email": r[2],
                "role": r[3]
            } for r in rows
        ]
@router.delete("/users/{user_id}")
def delete_user(user_id: int, admin_data=Depends(verify_admin)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if user exists before deleting
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Perform the deletion
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        
        return {"message": f"User '{user[0]}' (ID: {user_id}) has been deleted"}