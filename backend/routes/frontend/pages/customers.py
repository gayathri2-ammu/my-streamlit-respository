import streamlit as st

from frontend.api import (
    get_customers,
    create_customer,
    update_customer,
    delete_customer
)


def show_customers():

    st.title("👥 Customer Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "Add Customer",
            "View / Edit Customers",
            "Delete Customer"
        ]
    )

    # =====================================================
    # ADD
    # =====================================================

    with tab1:

        st.subheader("Add New Customer")

        with st.form("add_customer"):

            name = st.text_input("Name")
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=18
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"]
            )

            phone = st.text_input("Phone")
            email = st.text_input("Email")
            address = st.text_area("Address")

            submitted = st.form_submit_button(
                "Add Customer"
            )

            if submitted:

                if not all([
                    name,
                    phone,
                    email,
                    address
                ]):
                    st.error(
                        "Please fill all required fields."
                    )

                else:

                    result = create_customer({
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "phone": phone,
                        "email": email,
                        "address": address
                    })

                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(
                            result["message"]
                        )

                        st.rerun()

    # =====================================================
    # VIEW / EDIT
    # =====================================================

    with tab2:

        customers = get_customers()

        if isinstance(customers, dict) and "error" in customers:
            st.error(customers["error"])
            return

        if not customers:
            st.info("No customers found.")
            return

        st.dataframe(
            customers,
            use_container_width=True
        )

        st.subheader("Edit Customer")

        customer_ids = [
            c["customer_id"]
            for c in customers
        ]

        selected_id = st.selectbox(
            "Select Customer",
            customer_ids
        )

        customer = next(
            c for c in customers
            if c["customer_id"] == selected_id
        )

        with st.form("edit_customer"):

            name = st.text_input(
                "Name",
                value=customer["name"]
            )

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=customer["age"]
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=[
                    "Male",
                    "Female",
                    "Other"
                ].index(customer["gender"])
            )

            phone = st.text_input(
                "Phone",
                value=customer["phone"]
            )

            email = st.text_input(
                "Email",
                value=customer["email"]
            )

            address = st.text_area(
                "Address",
                value=customer["address"]
            )

            submitted = st.form_submit_button(
                "Update Customer"
            )

            if submitted:

                result = update_customer(
                    selected_id,
                    {
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "phone": phone,
                        "email": email,
                        "address": address
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

        customers = get_customers()

        if isinstance(customers, dict) and "error" in customers:
            st.error(customers["error"])
            return

        if not customers:
            st.info("No customers available.")
            return

        selected_id = st.selectbox(
            "Select Customer to Delete",
            [
                c["customer_id"]
                for c in customers
            ],
            key="delete_customer"
        )

        if st.button(
            "Delete Customer",
            type="primary"
        ):

            result = delete_customer(
                selected_id
            )

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])
                st.rerun()