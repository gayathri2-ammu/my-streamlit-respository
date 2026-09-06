from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# =========================================================
# AUTHENTICATION
# =========================================================

class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


# =========================================================
# CUSTOMER
# =========================================================

class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=1, le=120)
    gender: str = Field(min_length=1)
    phone: str = Field(min_length=10, max_length=15)
    email: EmailStr
    address: str = Field(min_length=2)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(value) < 10 or len(value) > 15:
            raise ValueError("Phone number must contain 10 to 15 digits")

        return value


class CustomerUpdate(CustomerCreate):
    pass


# =========================================================
# ROOM
# =========================================================

class RoomCreate(BaseModel):
    room_number: str = Field(min_length=1, max_length=20)
    room_type: str
    price_per_night: float = Field(gt=0)
    room_status: str

    @field_validator("room_type")
    @classmethod
    def validate_room_type(cls, value):
        allowed = ["Single", "Double", "Deluxe", "Suite"]

        if value not in allowed:
            raise ValueError(
                f"Room type must be one of: {', '.join(allowed)}"
            )

        return value

    @field_validator("room_status")
    @classmethod
    def validate_room_status(cls, value):
        allowed = ["Available", "Occupied", "Maintenance"]

        if value not in allowed:
            raise ValueError(
                f"Room status must be one of: {', '.join(allowed)}"
            )

        return value


class RoomUpdate(RoomCreate):
    pass


# =========================================================
# BOOKING
# =========================================================

class BookingCreate(BaseModel):
    customer_id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    check_in_date: date
    check_out_date: date
    number_of_guests: int = Field(gt=0)
    booking_status: str

    @field_validator("booking_status")
    @classmethod
    def validate_booking_status(cls, value):
        allowed = [
            "Confirmed",
            "Checked-In",
            "Checked-Out",
            "Cancelled"
        ]

        if value not in allowed:
            raise ValueError(
                f"Booking status must be one of: {', '.join(allowed)}"
            )

        return value


class BookingUpdate(BookingCreate):
    pass


# =========================================================
# PAYMENT
# =========================================================

class PaymentCreate(BaseModel):
    booking_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    payment_method: str
    payment_date: date
    payment_status: str

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value):
        allowed = ["Cash", "UPI", "Card", "Net Banking"]

        if value not in allowed:
            raise ValueError(
                f"Payment method must be one of: {', '.join(allowed)}"
            )

        return value

    @field_validator("payment_status")
    @classmethod
    def validate_payment_status(cls, value):
        allowed = ["Paid", "Pending", "Failed"]

        if value not in allowed:
            raise ValueError(
                f"Payment status must be one of: {', '.join(allowed)}"
            )

        return value


class PaymentUpdate(PaymentCreate):
    pass


# =========================================================
# SERVICE
# =========================================================

class ServiceCreate(BaseModel):
    service_name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    description: Optional[str] = None
    service_status: str

    @field_validator("service_status")
    @classmethod
    def validate_service_status(cls, value):
        allowed = ["Available", "Unavailable"]

        if value not in allowed:
            raise ValueError(
                f"Service status must be one of: {', '.join(allowed)}"
            )

        return value


class ServiceUpdate(ServiceCreate):
    pass


# =========================================================
# BOOKING SERVICES
# =========================================================

class BookingServiceCreate(BaseModel):
    booking_id: int = Field(gt=0)
    service_id: int = Field(gt=0)