from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter(
    prefix="/booking-services",
    tags=["Booking Services"]
)


# Database connection
def get_connection():
    conn = sqlite3.connect("database/hotel.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Pydantic model
class BookingServiceCreate(BaseModel):
    booking_id: int
    service_id: int
    quantity: int = 1


# Add service to booking
@router.post("/")
def add_booking_service(data: BookingServiceCreate):

    if data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    conn = get_connection()

    # Check booking exists
    booking = conn.execute(
        """
        SELECT booking_id
        FROM Bookings
        WHERE booking_id = ?
        """,
        (data.booking_id,)
    ).fetchone()

    if booking is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Check service exists
    service = conn.execute(
        """
        SELECT service_id
        FROM Services
        WHERE service_id = ?
        """,
        (data.service_id,)
    ).fetchone()

    if service is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # Check if service is already added
    existing = conn.execute(
        """
        SELECT booking_service_id
        FROM Booking_Services
        WHERE booking_id = ?
        AND service_id = ?
        """,
        (data.booking_id, data.service_id)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="This service is already added to the booking"
        )

    # Insert
    cursor = conn.execute(
        """
        INSERT INTO Booking_Services
        (booking_id, service_id, quantity)
        VALUES (?, ?, ?)
        """,
        (
            data.booking_id,
            data.service_id,
            data.quantity
        )
    )

    conn.commit()

    booking_service_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Service added to booking successfully",
        "booking_service_id": booking_service_id
    }


# View all booking services
@router.get("/")
def get_booking_services():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            bs.booking_service_id,
            bs.booking_id,
            bs.service_id,
            s.service_name,
            s.price,
            bs.quantity,
            (s.price * bs.quantity) AS total_price
        FROM Booking_Services bs
        JOIN Services s
            ON bs.service_id = s.service_id
        ORDER BY bs.booking_service_id
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# View services for one booking
@router.get("/{booking_id}")
def get_services_for_booking(booking_id: int):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            bs.booking_service_id,
            bs.booking_id,
            bs.service_id,
            s.service_name,
            s.price,
            bs.quantity,
            (s.price * bs.quantity) AS total_price
        FROM Booking_Services bs
        JOIN Services s
            ON bs.service_id = s.service_id
        WHERE bs.booking_id = ?
        """,
        (booking_id,)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# Delete service from booking
@router.delete("/{booking_service_id}")
def delete_booking_service(booking_service_id: int):

    conn = get_connection()

    cursor = conn.execute(
        """
        DELETE FROM Booking_Services
        WHERE booking_service_id = ?
        """,
        (booking_service_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Booking service not found"
        )

    return {
        "message": "Service removed from booking successfully"
    }