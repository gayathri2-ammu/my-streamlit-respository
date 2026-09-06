import streamlit as st
import pandas as pd

from frontend.api import (
    get_monthly_revenue,
    get_most_booked_room,
    get_available_rooms,
    get_customers,
    get_customer_bookings,
    get_customer_payments
)


def show_reports():

    st.title("📈 Reports")

    # =====================================================
    # MONTHLY REVENUE
    # =====================================================

    st.subheader("Monthly Revenue")

    revenue = get_monthly_revenue()

    if isinstance(revenue, dict):
        st.error(revenue.get("error"))
    elif revenue:

        df = pd.DataFrame(revenue)

        df = df.set_index("month")

        st.line_chart(
            df["revenue"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.info(
            "No revenue data available."
        )

    st.divider()

    # =====================================================
    # MOST BOOKED ROOM
    # =====================================================

    st.subheader("⭐ Most Booked Room")

    most_booked = get_most_booked_room()

    if "error" in most_booked:
        st.error(most_booked["error"])

    elif "message" in most_booked:
        st.info(most_booked["message"])

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Room",
            most_booked["room_number"]
        )

        col2.metric(
            "Type",
            most_booked["room_type"]
        )

        col3.metric(
            "Bookings",
            most_booked["booking_count"]
        )

    st.divider()

    # =====================================================
    # AVAILABLE ROOMS
    # =====================================================

    st.subheader("🛏️ Available Rooms")

    rooms = get_available_rooms()

    if isinstance(rooms, dict):
        st.error(rooms.get("error"))

    elif rooms:
        st.dataframe(
            rooms,
            use_container_width=True
        )

    else:
        st.info(
            "No available rooms."
        )

    st.divider()

    # =====================================================
    # CUSTOMER HISTORY
    # =====================================================

    st.subheader("👤 Customer History")

    customers = get_customers()

    if isinstance(customers, dict):
        st.error(customers.get("error"))
        return

    if not customers:
        st.info("No customers available.")
        return

    customer_options = {
        f"{c['customer_id']} - {c['name']}":
            c["customer_id"]
        for c in customers
    }

    selected_customer = st.selectbox(
        "Select Customer",
        list(customer_options.keys())
    )

    customer_id = customer_options[
        selected_customer
    ]

    history_tab1, history_tab2 = st.tabs(
        [
            "Booking History",
            "Payment History"
        ]
    )

    with history_tab1:

        bookings = get_customer_bookings(
            customer_id
        )

        if isinstance(bookings, dict):
            st.error(bookings.get("error"))

        elif bookings:
            st.dataframe(
                bookings,
                use_container_width=True
            )

        else:
            st.info(
                "No booking history."
            )

    with history_tab2:

        payments = get_customer_payments(
            customer_id
        )

        if isinstance(payments, dict):
            st.error(payments.get("error"))

        elif payments:
            st.dataframe(
                payments,
                use_container_width=True
            )

        else:
            st.info(
                "No payment history."
            )