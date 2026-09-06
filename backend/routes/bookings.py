from fastapi import APIRouter, HTTPException

from backend.database import get_db
from backend.schemas import BookingCreate, BookingUpdate

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def validate_booking(conn, data, booking_id=None):

    # ---------------------------------------------
    # Check customer
    # ---------------------------------------------

    customer = conn.execute(
        """
        SELECT customer_id
        FROM Customers
        WHERE customer_id = ?
        """,
        (data.customer_id,)
    ).fetchone()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # ---------------------------------------------
    # Check room
    # ---------------------------------------------

    room = conn.execute(
        """
        SELECT room_id, room_status
        FROM Rooms
        WHERE room_id = ?
        """,
        (data.room_id,)
    ).fetchone()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if room["room_status"] == "Maintenance":
        raise HTTPException(
            status_code=409,
            detail="Room is under maintenance"
        )

    # ---------------------------------------------
    # Check dates
    # ---------------------------------------------

    if data.check_out_date <= data.check_in_date:
        raise HTTPException(
            status_code=400,
            detail="Check-out date must be after check-in date"
        )

    # ---------------------------------------------
    # Check room availability
    # ---------------------------------------------

    query = """
        SELECT booking_id
        FROM Bookings
        WHERE room_id = ?
        AND booking_status IN ('Confirmed', 'Checked-In')
        AND check_in_date < ?
        AND check_out_date > ?
    """

    params = [
        data.room_id,
        data.check_out_date.isoformat(),
        data.check_in_date.isoformat()
    ]

    if booking_id is not None:
        query += " AND booking_id != ?"
        params.append(booking_id)

    existing = conn.execute(
        query,
        tuple(params)
    ).fetchone()

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Room is unavailable for the selected dates"
        )


# =========================================================
# GET ALL BOOKINGS
# =========================================================

@router.get("/")
def get_bookings():

    conn = get_db()

    try:

        rows = conn.execute(
            """
            SELECT
                b.booking_id,
                b.customer_id,
                c.name AS customer_name,
                b.room_id,
                r.room_number,
                r.room_type,
                r.price_per_night,
                b.check_in_date,
                b.check_out_date,
                b.number_of_guests,
                b.booking_status
            FROM Bookings b
            JOIN Customers c
                ON b.customer_id = c.customer_id
            JOIN Rooms r
                ON b.room_id = r.room_id
            ORDER BY b.booking_id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


# =========================================================
# GET BOOKING
# =========================================================

@router.get("/{booking_id}")
def get_booking(booking_id: int):

    conn = get_db()

    try:

        row = conn.execute(
            """
            SELECT
                b.booking_id,
                b.customer_id,
                c.name AS customer_name,
                b.room_id,
                r.room_number,
                r.room_type,
                b.check_in_date,
                b.check_out_date,
                b.number_of_guests,
                b.booking_status
            FROM Bookings b
            JOIN Customers c
                ON b.customer_id = c.customer_id
            JOIN Rooms r
                ON b.room_id = r.room_id
            WHERE b.booking_id = ?
            """,
            (booking_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return dict(row)

    finally:
        conn.close()


# =========================================================
# CREATE BOOKING
# =========================================================

@router.post("/", status_code=201)
def create_booking(data: BookingCreate):

    conn = get_db()

    try:

        validate_booking(conn, data)

        cursor = conn.execute(
            """
            INSERT INTO Bookings
            (
                customer_id,
                room_id,
                check_in_date,
                check_out_date,
                number_of_guests,
                booking_status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.customer_id,
                data.room_id,
                data.check_in_date.isoformat(),
                data.check_out_date.isoformat(),
                data.number_of_guests,
                data.booking_status
            )
        )

        conn.commit()

        return {
            "message": "Booking created successfully",
            "booking_id": cursor.lastrowid
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


# =========================================================
# UPDATE BOOKING
# =========================================================

@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    data: BookingUpdate
):

    conn = get_db()

    try:

        booking = conn.execute(
            """
            SELECT booking_id
            FROM Bookings
            WHERE booking_id = ?
            """,
            (booking_id,)
        ).fetchone()

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        validate_booking(
            conn,
            data,
            booking_id
        )

        conn.execute(
            """
            UPDATE Bookings
            SET
                customer_id = ?,
                room_id = ?,
                check_in_date = ?,
                check_out_date = ?,
                number_of_guests = ?,
                booking_status = ?
            WHERE booking_id = ?
            """,
            (
                data.customer_id,
                data.room_id,
                data.check_in_date.isoformat(),
                data.check_out_date.isoformat(),
                data.number_of_guests,
                data.booking_status,
                booking_id
            )
        )

        conn.commit()

        return {
            "message": "Booking updated successfully"
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


# =========================================================
# DELETE BOOKING
# =========================================================

@router.delete("/{booking_id}")
def delete_booking(booking_id: int):

    conn = get_db()

    try:

        booking = conn.execute(
            """
            SELECT booking_id
            FROM Bookings
            WHERE booking_id = ?
            """,
            (booking_id,)
        ).fetchone()

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        conn.execute(
            """
            DELETE FROM Bookings
            WHERE booking_id = ?
            """,
            (booking_id,)
        )

        conn.commit()

        return {
            "message": "Booking deleted successfully"
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