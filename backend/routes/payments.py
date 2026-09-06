from fastapi import APIRouter, HTTPException

from backend.database import get_db
from backend.schemas import PaymentCreate, PaymentUpdate

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def validate_payment(conn, data):

    booking = conn.execute(
        """
        SELECT booking_id, customer_id
        FROM Bookings
        WHERE booking_id = ?
        """,
        (data.booking_id,)
    ).fetchone()

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

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

    if booking["customer_id"] != data.customer_id:
        raise HTTPException(
            status_code=400,
            detail="Customer does not belong to this booking"
        )


@router.get("/")
def get_payments():

    conn = get_db()

    try:

        rows = conn.execute(
            """
            SELECT
                p.payment_id,
                p.booking_id,
                p.customer_id,
                c.name AS customer_name,
                p.amount,
                p.payment_method,
                p.payment_date,
                p.payment_status
            FROM Payments p
            JOIN Customers c
                ON p.customer_id = c.customer_id
            ORDER BY p.payment_id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@router.get("/{payment_id}")
def get_payment(payment_id: int):

    conn = get_db()

    try:

        row = conn.execute(
            """
            SELECT
                p.*,
                c.name AS customer_name
            FROM Payments p
            JOIN Customers c
                ON p.customer_id = c.customer_id
            WHERE p.payment_id = ?
            """,
            (payment_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return dict(row)

    finally:
        conn.close()


@router.post("/", status_code=201)
def create_payment(data: PaymentCreate):

    conn = get_db()

    try:

        validate_payment(conn, data)

        cursor = conn.execute(
            """
            INSERT INTO Payments
            (
                booking_id,
                customer_id,
                amount,
                payment_method,
                payment_date,
                payment_status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.booking_id,
                data.customer_id,
                data.amount,
                data.payment_method,
                data.payment_date.isoformat(),
                data.payment_status
            )
        )

        conn.commit()

        return {
            "message": "Payment created successfully",
            "payment_id": cursor.lastrowid
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


@router.put("/{payment_id}")
def update_payment(
    payment_id: int,
    data: PaymentUpdate
):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT payment_id
            FROM Payments
            WHERE payment_id = ?
            """,
            (payment_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        validate_payment(conn, data)

        conn.execute(
            """
            UPDATE Payments
            SET
                booking_id = ?,
                customer_id = ?,
                amount = ?,
                payment_method = ?,
                payment_date = ?,
                payment_status = ?
            WHERE payment_id = ?
            """,
            (
                data.booking_id,
                data.customer_id,
                data.amount,
                data.payment_method,
                data.payment_date.isoformat(),
                data.payment_status,
                payment_id
            )
        )

        conn.commit()

        return {
            "message": "Payment updated successfully"
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


@router.delete("/{payment_id}")
def delete_payment(payment_id: int):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT payment_id
            FROM Payments
            WHERE payment_id = ?
            """,
            (payment_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        conn.execute(
            """
            DELETE FROM Payments
            WHERE payment_id = ?
            """,
            (payment_id,)
        )

        conn.commit()

        return {
            "message": "Payment deleted successfully"
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