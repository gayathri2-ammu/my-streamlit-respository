from fastapi import APIRouter, HTTPException

from backend.database import get_db
from backend.schemas import ServiceCreate, ServiceUpdate

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.get("/")
def get_services():

    conn = get_db()

    try:

        rows = conn.execute(
            """
            SELECT *
            FROM Services
            ORDER BY service_id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@router.get("/{service_id}")
def get_service(service_id: int):

    conn = get_db()

    try:

        row = conn.execute(
            """
            SELECT *
            FROM Services
            WHERE service_id = ?
            """,
            (service_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        return dict(row)

    finally:
        conn.close()


@router.post("/", status_code=201)
def create_service(data: ServiceCreate):

    conn = get_db()

    try:

        cursor = conn.execute(
            """
            INSERT INTO Services
            (
                service_name,
                price,
                description,
                service_status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                data.service_name,
                data.price,
                data.description,
                data.service_status
            )
        )

        conn.commit()

        return {
            "message": "Service created successfully",
            "service_id": cursor.lastrowid
        }

    except Exception as e:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:
        conn.close()


@router.put("/{service_id}")
def update_service(
    service_id: int,
    data: ServiceUpdate
):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT service_id
            FROM Services
            WHERE service_id = ?
            """,
            (service_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        conn.execute(
            """
            UPDATE Services
            SET
                service_name = ?,
                price = ?,
                description = ?,
                service_status = ?
            WHERE service_id = ?
            """,
            (
                data.service_name,
                data.price,
                data.description,
                data.service_status,
                service_id
            )
        )

        conn.commit()

        return {
            "message": "Service updated successfully"
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


@router.delete("/{service_id}")
def delete_service(service_id: int):

    conn = get_db()

    try:

        existing = conn.execute(
            """
            SELECT service_id
            FROM Services
            WHERE service_id = ?
            """,
            (service_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        conn.execute(
            """
            DELETE FROM Services
            WHERE service_id = ?
            """,
            (service_id,)
        )

        conn.commit()

        return {
            "message": "Service deleted successfully"
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