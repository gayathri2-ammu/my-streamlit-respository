from fastapi import APIRouter, HTTPException

from backend.database import get_db
from backend.schemas import LoginRequest



router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(data: LoginRequest):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            SELECT user_id, username
            FROM Users
            WHERE username = ?
            AND password = ?
            """,
            (data.username, data.password)
        )

        user = cursor.fetchone()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        return {
            "message": "Login successful",
            "user_id": user["user_id"],
            "username": user["username"]
        }

    finally:
        conn.close()