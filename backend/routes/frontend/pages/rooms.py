import streamlit as st

from frontend.api import (
    get_rooms,
    create_room,
    update_room,
    delete_room
)


def show_rooms():

    st.title("🛏️ Room Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "Add Room",
            "View / Edit Rooms",
            "Delete Room"
        ]
    )

    # =====================================================
    # ADD ROOM
    # =====================================================

    with tab1:

        with st.form("add_room"):

            room_number = st.text_input(
                "Room Number"
            )

            room_type = st.selectbox(
                "Room Type",
                [
                    "Single",
                    "Double",
                    "Deluxe",
                    "Suite"
                ]
            )

            price = st.number_input(
                "Price Per Night",
                min_value=1.0,
                step=100.0
            )

            status = st.selectbox(
                "Room Status",
                [
                    "Available",
                    "Occupied",
                    "Maintenance"
                ]
            )

            submitted = st.form_submit_button(
                "Add Room"
            )

            if submitted:

                if not room_number:
                    st.error(
                        "Room number is required."
                    )
                    return

                result = create_room({
                    "room_number": room_number,
                    "room_type": room_type,
                    "price_per_night": price,
                    "room_status": status
                })

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(result["message"])
                    st.rerun()

    # =====================================================
    # VIEW / EDIT
    # =====================================================

    with tab2:

        rooms = get_rooms()

        if isinstance(rooms, dict) and "error" in rooms:
            st.error(rooms["error"])
            return

        if not rooms:
            st.info("No rooms found.")
            return

        st.dataframe(
            rooms,
            use_container_width=True
        )

        room_ids = [
            r["room_id"]
            for r in rooms
        ]

        selected_id = st.selectbox(
            "Select Room",
            room_ids,
            key="edit_room"
        )

        room = next(
            r for r in rooms
            if r["room_id"] == selected_id
        )

        with st.form("update_room"):

            room_number = st.text_input(
                "Room Number",
                value=room["room_number"]
            )

            room_type = st.selectbox(
                "Room Type",
                [
                    "Single",
                    "Double",
                    "Deluxe",
                    "Suite"
                ],
                index=[
                    "Single",
                    "Double",
                    "Deluxe",
                    "Suite"
                ].index(room["room_type"])
            )

            price = st.number_input(
                "Price Per Night",
                min_value=1.0,
                value=float(
                    room["price_per_night"]
                )
            )

            status = st.selectbox(
                "Room Status",
                [
                    "Available",
                    "Occupied",
                    "Maintenance"
                ],
                index=[
                    "Available",
                    "Occupied",
                    "Maintenance"
                ].index(room["room_status"])
            )

            submitted = st.form_submit_button(
                "Update Room"
            )

            if submitted:

                result = update_room(
                    selected_id,
                    {
                        "room_number": room_number,
                        "room_type": room_type,
                        "price_per_night": price,
                        "room_status": status
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

        rooms = get_rooms()

        if not rooms:
            st.info("No rooms available.")
            return

        selected_id = st.selectbox(
            "Select Room to Delete",
            [
                r["room_id"]
                for r in rooms
            ],
            key="delete_room"
        )

        if st.button(
            "Delete Room",
            type="primary"
        ):

            result = delete_room(
                selected_id
            )

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])
                st.rerun()