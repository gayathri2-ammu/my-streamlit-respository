from fastapi import APIRouter, HTTPException

from backend.database import get_db
from backend.schemas import CustomerCreate, CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# =========================================================
# GET ALL CUSTOMERS
# =========================================================

@router.get("/")
def get_customers():

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            SELECT *
            FROM Customers
            ORDER BY customer_id DESC
            """
        )

        customers = cursor.fetchall()

        return [dict(customer) for customer in customers]

    finally:
        conn.close()


# =========================================================
# GET CUSTOMER BY ID
# =========================================================

@router.get("/{customer_id}")
def get_customer(customer_id: int):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            SELECT *
            FROM Customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return dict(customer)

    finally:
        conn.close()


# =========================================================
# CREATE CUSTOMER
# =========================================================

@router.post("/", status_code=201)
def create_customer(data: CustomerCreate):

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO Customers
            (name, age, gender, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.name,
                data.age,
                data.gender,
                data.phone,
                data.email,
                data.address
            )
        )

        conn.commit()

        return {
            "message": "Customer created successfully",
            "customer_id": cursor.lastrowid
        }

    except Exception as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:
        conn.close()


# =========================================================
# UPDATE CUSTOMER
# =========================================================

@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    data: CustomerUpdate
):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT customer_id
            FROM Customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        conn.execute(
            """
            UPDATE Customers
            SET
                name = ?,
                age = ?,
                gender = ?,
                phone = ?,
                email = ?,
                address = ?
            WHERE customer_id = ?
            """,
            (
                data.name,
                data.age,
                data.gender,
                data.phone,
                data.email,
                data.address,
                customer_id
            )
        )

        conn.commit()

        return {
            "message": "Customer updated successfully"
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
# DELETE CUSTOMER
# =========================================================

@router.delete("/{customer_id}")
def delete_customer(customer_id: int):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT customer_id
            FROM Customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        conn.execute(
            """
            DELETE FROM Customers
            WHERE customer_id = ?
            """,
            (customer_id,)
        )

        conn.commit()

        return {
            "message": "Customer deleted successfully"
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