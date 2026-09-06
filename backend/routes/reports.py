from fastapi import APIRouter, HTTPException

from backend.database import get_db

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# =========================================================
# DASHBOARD
# =========================================================

@router.get("/dashboard")
def dashboard():

    conn = get_db()

    try:

        customers = conn.execute(
            "SELECT COUNT(*) AS total FROM Customers"
        ).fetchone()["total"]

        rooms = conn.execute(
            "SELECT COUNT(*) AS total FROM Rooms"
        ).fetchone()["total"]

        bookings = conn.execute(
            "SELECT COUNT(*) AS total FROM Bookings"
        ).fetchone()["total"]

        revenue = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM Payments
            WHERE payment_status = 'Paid'
            """
        ).fetchone()["total"]

        return {
            "total_customers": customers,
            "total_rooms": rooms,
            "total_bookings": bookings,
            "total_revenue": revenue
        }

    finally:
        conn.close()


# =========================================================
# MONTHLY REVENUE
# =========================================================

@router.get("/monthly-revenue")
def monthly_revenue():

    conn = get_db()

    try:

        rows = conn.execute(
            """
            SELECT
                substr(payment_date, 1, 7) AS month,
                SUM(amount) AS revenue
            FROM Payments
            WHERE payment_status = 'Paid'
            GROUP BY substr(payment_date, 1, 7)
            ORDER BY month
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


# =========================================================
# MOST BOOKED ROOM
# =========================================================

@router.get("/most-booked-room")
def most_booked_room():

    conn = get_db()

    try:

        row = conn.execute(
            """
            SELECT
                r.room_number,
                r.room_type,
                COUNT(b.booking_id) AS booking_count
            FROM Rooms r
            JOIN Bookings b
                ON r.room_id = b.room_id
            WHERE b.booking_status != 'Cancelled'
            GROUP BY r.room_id
            ORDER BY booking_count DESC
            LIMIT 1
            """
        ).fetchone()

        if row is None:
            return {
                "message": "No bookings available"
            }

        return dict(row)

    finally:
        conn.close()


# =========================================================
# AVAILABLE ROOMS
# =========================================================

@router.get("/available-rooms")
def available_rooms():

    conn = get_db()

    try:

        rows = conn.execute(
            """
            SELECT *
            FROM Rooms
            WHERE room_status = 'Available'
            ORDER BY room_number
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


# =========================================================
# CUSTOMER BOOKING HISTORY
# =========================================================

@router.get("/customer/{customer_id}/bookings")
def customer_booking_history(customer_id: int):

    conn = get_db()

    try:

        customer = conn.execute(
            """
            SELECT customer_id
            FROM Customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        ).fetchone()

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        rows = conn.execute(
            """
            SELECT
                b.booking_id,
                c.name AS customer_name,
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
            WHERE b.customer_id = ?
            ORDER BY b.booking_id DESC
            """,
            (customer_id,)
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


# =========================================================
# CUSTOMER PAYMENT HISTORY
# =========================================================

@router.get("/customer/{customer_id}/payments")
def customer_payment_history(customer_id: int):

    conn = get_db()

    try:

        customer = conn.execute(
            """
            SELECT customer_id
            FROM Customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        ).fetchone()

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        rows = conn.execute(
            """
            SELECT
                p.payment_id,
                p.booking_id,
                c.name AS customer_name,
                p.amount,
                p.payment_method,
                p.payment_date,
                p.payment_status
            FROM Payments p
            JOIN Customers c
                ON p.customer_id = c.customer_id
            WHERE p.customer_id = ?
            ORDER BY p.payment_id DESC
            """,
            (customer_id,)
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()