import streamlit as st
from datetime import date

from frontend.api import (
    get_payments,
    create_payment,
    update_payment,
    delete_payment,
    get_bookings,
    get_customers
)


def show_payments():

    st.title("💳 Payment Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "Add Payment",
            "View / Edit Payments",
            "Delete Payment"
        ]
    )

    # =====================================================
    # ADD PAYMENT
    # =====================================================

    with tab1:

        bookings = get_bookings()
        customers = get_customers()

        if isinstance(bookings, dict):
            st.error(bookings.get("error"))
            return

        if isinstance(customers, dict):
            st.error(customers.get("error"))
            return

        if not bookings:
            st.warning(
                "Create a booking before adding a payment."
            )
            return

        booking_options = {
            f"Booking #{b['booking_id']} - "
            f"{b['customer_name']} - "
            f"Room {b['room_number']}":
                b
            for b in bookings
        }

        with st.form("add_payment"):

            booking_label = st.selectbox(
                "Booking",
                list(booking_options.keys())
            )

            selected_booking = booking_options[
                booking_label
            ]

            st.info(
                f"Customer: "
                f"{selected_booking['customer_name']}"
            )

            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=100.0
            )

            method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Card",
                    "Net Banking"
                ]
            )

            payment_date = st.date_input(
                "Payment Date",
                value=date.today()
            )

            status = st.selectbox(
                "Payment Status",
                [
                    "Paid",
                    "Pending",
                    "Failed"
                ]
            )

            submitted = st.form_submit_button(
                "Add Payment"
            )

            if submitted:

                result = create_payment({
                    "booking_id":
                        selected_booking["booking_id"],

                    "customer_id":
                        selected_booking["customer_id"],

                    "amount":
                        amount,

                    "payment_method":
                        method,

                    "payment_date":
                        payment_date.isoformat(),

                    "payment_status":
                        status
                })

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
                    st.rerun()

    # =====================================================
    # VIEW
    # =====================================================

    with tab2:

        payments = get_payments()

        if isinstance(payments, dict):
            st.error(payments.get("error"))
            return

        if not payments:
            st.info("No payments found.")
            return

        st.dataframe(
            payments,
            use_container_width=True
        )

        payment_ids = [
            p["payment_id"]
            for p in payments
        ]

        selected_id = st.selectbox(
            "Payment ID",
            payment_ids,
            key="edit_payment"
        )

        payment = next(
            p for p in payments
            if p["payment_id"] == selected_id
        )

        with st.form("edit_payment"):

            amount = st.number_input(
                "Amount",
                min_value=0.01,
                value=float(payment["amount"])
            )

            method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Card",
                    "Net Banking"
                ],
                index=[
                    "Cash",
                    "UPI",
                    "Card",
                    "Net Banking"
                ].index(
                    payment["payment_method"]
                )
            )

            status = st.selectbox(
                "Payment Status",
                [
                    "Paid",
                    "Pending",
                    "Failed"
                ],
                index=[
                    "Paid",
                    "Pending",
                    "Failed"
                ].index(
                    payment["payment_status"]
                )
            )

            submitted = st.form_submit_button(
                "Update Payment"
            )

            if submitted:

                result = update_payment(
                    selected_id,
                    {
                        "booking_id":
                            payment["booking_id"],

                        "customer_id":
                            payment["customer_id"],

                        "amount":
                            amount,

                        "payment_method":
                            method,

                        "payment_date":
                            payment["payment_date"],

                        "payment_status":
                            status
                    }
                )

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
                    st.rerun()

    # =====================================================
    # DELETE
    # =====================================================

    with tab3:

        payments = get_payments()

        if not payments:
            st.info("No payments available.")
            return

        selected_id = st.selectbox(
            "Payment ID",
            [
                p["payment_id"]
                for p in payments
            ],
            key="delete_payment"
        )

        if st.button(
            "Delete Payment",
            type="primary"
        ):

            result = delete_payment(
                selected_id
            )

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])
                st.rerun()