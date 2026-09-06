import requests

BASE_URL = "http://127.0.0.1:8000"


def get_request(endpoint):
    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }


def post_request(endpoint, data):
    try:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            json=data,
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        try:
            return {
                "error": response.json().get(
                    "detail",
                    "Request failed"
                )
            }
        except Exception:
            return {
                "error": "Request failed"
            }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }


def put_request(endpoint, data):
    try:
        response = requests.put(
            f"{BASE_URL}{endpoint}",
            json=data,
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        try:
            return {
                "error": response.json().get(
                    "detail",
                    "Request failed"
                )
            }
        except Exception:
            return {
                "error": "Request failed"
            }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }


def delete_request(endpoint):
    try:
        response = requests.delete(
            f"{BASE_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        try:
            return {
                "error": response.json().get(
                    "detail",
                    "Request failed"
                )
            }
        except Exception:
            return {
                "error": "Request failed"
            }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }


# =========================================================
# AUTHENTICATION
# =========================================================

def login(username, password):

    return post_request(
        "/auth/login",
        {
            "username": username,
            "password": password
        }
    )


# =========================================================
# CUSTOMERS
# =========================================================

def get_customers():
    return get_request("/customers/")


def create_customer(data):
    return post_request("/customers/", data)


def update_customer(customer_id, data):
    return put_request(
        f"/customers/{customer_id}",
        data
    )


def delete_customer(customer_id):
    return delete_request(
        f"/customers/{customer_id}"
    )


# =========================================================
# ROOMS
# =========================================================

def get_rooms():
    return get_request("/rooms/")


def create_room(data):
    return post_request("/rooms/", data)


def update_room(room_id, data):
    return put_request(
        f"/rooms/{room_id}",
        data
    )


def delete_room(room_id):
    return delete_request(
        f"/rooms/{room_id}"
    )


# =========================================================
# BOOKINGS
# =========================================================

def get_bookings():
    return get_request("/bookings/")


def create_booking(data):
    return post_request("/bookings/", data)


def update_booking(booking_id, data):
    return put_request(
        f"/bookings/{booking_id}",
        data
    )


def delete_booking(booking_id):
    return delete_request(
        f"/bookings/{booking_id}"
    )


# =========================================================
# PAYMENTS
# =========================================================

def get_payments():
    return get_request("/payments/")


def create_payment(data):
    return post_request("/payments/", data)


def update_payment(payment_id, data):
    return put_request(
        f"/payments/{payment_id}",
        data
    )


def delete_payment(payment_id):
    return delete_request(
        f"/payments/{payment_id}"
    )


# =========================================================
# SERVICES
# =========================================================

def get_services():
    return get_request("/services/")


def create_service(data):
    return post_request("/services/", data)


def update_service(service_id, data):
    return put_request(
        f"/services/{service_id}",
        data
    )


def delete_service(service_id):
    return delete_request(
        f"/services/{service_id}"
    )


# =========================================================
# REPORTS
# =========================================================

def get_dashboard():
    return get_request("/reports/dashboard")


def get_monthly_revenue():
    return get_request(
        "/reports/monthly-revenue"
    )


def get_most_booked_room():
    return get_request(
        "/reports/most-booked-room"
    )


def get_available_rooms():
    return get_request(
        "/reports/available-rooms"
    )


def get_customer_bookings(customer_id):
    return get_request(
        f"/reports/customer/{customer_id}/bookings"
    )


def get_customer_payments(customer_id):
    return get_request(
        f"/reports/customer/{customer_id}/payments"
    )