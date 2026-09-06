import streamlit as st
from datetime import date

from api import (
    get_bookings,
    create_booking,
    update_booking,
    delete_booking,
    get_customers,
    get_rooms
)


def show_bookings():

    st.title("📅 Booking Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "Create Booking",
            "View / Edit Bookings",
            "Delete Booking"
        ]
    )

    # =====================================================
    # CREATE BOOKING
    # =====================================================

    with tab1:

        customers = get_customers()
        rooms = get_rooms()

        if isinstance(customers, dict):
            st.error(customers.get("error"))
            return

        if isinstance(rooms, dict):
            st.error(rooms.get("error"))
            return

        if not customers:
            st.warning(
                "Please add a customer first."
            )
            return

        if not rooms:
            st.warning(
                "Please add a room first."
            )
            return

        customer_options = {
            f"{c['customer_id']} - {c['name']}":
                c["customer_id"]
            for c in customers
        }

        room_options = {
            f"{r['room_id']} - Room {r['room_number']} "
            f"({r['room_type']})":
                r["room_id"]
            for r in rooms
            if r["room_status"] != "Maintenance"
        }

        if not room_options:
            st.warning(
                "No rooms are currently available."
            )
            return

        with st.form("create_booking"):

            customer_label = st.selectbox(
                "Customer",
                list(customer_options.keys())
            )

            room_label = st.selectbox(
                "Room",
                list(room_options.keys())
            )

            check_in = st.date_input(
                "Check-in Date",
                value=date.today()
            )

            check_out = st.date_input(
                "Check-out Date"
            )

            guests = st.number_input(
                "Number of Guests",
                min_value=1,
                value=1
            )

            status = st.selectbox(
                "Booking Status",
                [
                    "Confirmed",
                    "Checked-In",
                    "Checked-Out",
                    "Cancelled"
                ]
            )

            submitted = st.form_submit_button(
                "Create Booking"
            )

            if submitted:

                if check_out <= check_in:
                    st.error(
                        "Check-out must be after check-in."
                    )
                    return

                result = create_booking({
                    "customer_id":
                        customer_options[customer_label],

                    "room_id":
                        room_options[room_label],

                    "check_in_date":
                        check_in.isoformat(),

                    "check_out_date":
                        check_out.isoformat(),

                    "number_of_guests":
                        guests,

                    "booking_status":
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

        bookings = get_bookings()

        if isinstance(bookings, dict):
            st.error(bookings.get("error"))
            return

        if not bookings:
            st.info("No bookings found.")
            return

        st.dataframe(
            bookings,
            use_container_width=True
        )

        st.subheader("Edit Booking")

        booking_ids = [
            b["booking_id"]
            for b in bookings
        ]

        selected_id = st.selectbox(
            "Booking ID",
            booking_ids,
            key="edit_booking"
        )

        booking = next(
            b for b in bookings
            if b["booking_id"] == selected_id
        )

        customers = get_customers()
        rooms = get_rooms()

        customer_options = {
            f"{c['customer_id']} - {c['name']}":
                c["customer_id"]
            for c in customers
        }

        room_options = {
            f"{r['room_id']} - Room {r['room_number']}":
                r["room_id"]
            for r in rooms
        }

        current_customer = next(
            label
            for label, cid in customer_options.items()
            if cid == booking["customer_id"]
        )

        current_room = next(
            label
            for label, rid in room_options.items()
            if rid == booking["room_id"]
        )

        with st.form("edit_booking"):

            customer_label = st.selectbox(
                "Customer",
                list(customer_options.keys()),
                index=list(
                    customer_options.keys()
                ).index(current_customer)
            )

            room_label = st.selectbox(
                "Room",
                list(room_options.keys()),
                index=list(
                    room_options.keys()
                ).index(current_room)
            )

            check_in = st.date_input(
                "Check-in",
                value=date.fromisoformat(
                    booking["check_in_date"]
                )
            )

            check_out = st.date_input(
                "Check-out",
                value=date.fromisoformat(
                    booking["check_out_date"]
                )
            )

            guests = st.number_input(
                "Guests",
                min_value=1,
                value=booking["number_of_guests"]
            )

            status = st.selectbox(
                "Status",
                [
                    "Confirmed",
                    "Checked-In",
                    "Checked-Out",
                    "Cancelled"
                ],
                index=[
                    "Confirmed",
                    "Checked-In",
                    "Checked-Out",
                    "Cancelled"
                ].index(
                    booking["booking_status"]
                )
            )

            submitted = st.form_submit_button(
                "Update Booking"
            )

            if submitted:

                result = update_booking(
                    selected_id,
                    {
                        "customer_id":
                            customer_options[customer_label],

                        "room_id":
                            room_options[room_label],

                        "check_in_date":
                            check_in.isoformat(),

                        "check_out_date":
                            check_out.isoformat(),

                        "number_of_guests":
                            guests,

                        "booking_status":
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

        bookings = get_bookings()

        if not bookings:
            st.info("No bookings available.")
            return

        selected_id = st.selectbox(
            "Booking ID",
            [
                b["booking_id"]
                for b in bookings
            ],
            key="delete_booking"
        )

        if st.button(
            "Delete Booking",
            type="primary"
        ):

            result = delete_booking(
                selected_id
            )

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])
                st.rerun()