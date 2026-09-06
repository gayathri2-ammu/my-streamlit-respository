from fastapi import APIRouter, HTTPException
from backend.database import get_connection


from backend.database import get_db
from backend.schemas import RoomCreate, RoomUpdate

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/")
def get_rooms():

    conn = get_db()

    try:
        rows = conn.execute(
            """
            SELECT *
            FROM Rooms
            ORDER BY room_id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@router.get("/{room_id}")
def get_room(room_id: int):

    conn = get_db()

    try:
        row = conn.execute(
            """
            SELECT *
            FROM Rooms
            WHERE room_id = ?
            """,
            (room_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Room not found"
            )

        return dict(row)

    finally:
        conn.close()


@router.post("/", status_code=201)
def create_room(data: RoomCreate):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT room_id
            FROM Rooms
            WHERE room_number = ?
            """,
            (data.room_number,)
        ).fetchone()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Room number already exists"
            )

        cursor = conn.execute(
            """
            INSERT INTO Rooms
            (
                room_number,
                room_type,
                price_per_night,
                room_status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                data.room_number,
                data.room_type,
                data.price_per_night,
                data.room_status
            )
        )

        conn.commit()

        return {
            "message": "Room created successfully",
            "room_id": cursor.lastrowid
        }

    except HTTPException:
        raise

    except Exception as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:
        conn.close()


@router.put("/{room_id}")
def update_room(
    room_id: int,
    data: RoomUpdate
):

    conn = get_db()

    try:

        room = conn.execute(
            """
            SELECT room_id
            FROM Rooms
            WHERE room_id = ?
            """,
            (room_id,)
        ).fetchone()

        if room is None:
            raise HTTPException(
                status_code=404,
                detail="Room not found"
            )

        duplicate = conn.execute(
            """
            SELECT room_id
            FROM Rooms
            WHERE room_number = ?
            AND room_id != ?
            """,
            (data.room_number, room_id)
        ).fetchone()

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Room number already exists"
            )

        conn.execute(
            """
            UPDATE Rooms
            SET
                room_number = ?,
                room_type = ?,
                price_per_night = ?,
                room_status = ?
            WHERE room_id = ?
            """,
            (
                data.room_number,
                data.room_type,
                data.price_per_night,
                data.room_status,
                room_id
            )
        )

        conn.commit()

        return {
            "message": "Room updated successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:
        conn.close()


@router.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    conn = get_connection()

    booking = conn.execute(
        """
        SELECT booking_id
        FROM Bookings
        WHERE room_id = ?
        LIMIT 1
        """,
        (room_id,)
    ).fetchone()

    if booking:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete room because bookings exist for this room"
        )

    cursor = conn.execute(
        "DELETE FROM Rooms WHERE room_id = ?",
        (room_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return {"message": "Room deleted successfully"}