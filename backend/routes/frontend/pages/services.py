import streamlit as st
from frontend.api import (
    get_services,
    create_service,
    update_service,
    delete_service
)

def show_services():
    st.title("Hotel Services")

    st.subheader("Add Service")

    service_name = st.text_input("Service Name")
    price = st.number_input("Price", min_value=0.0)
    description = st.text_area("Description")

    service_status = st.selectbox(
        "Service Status",
        ["Available", "Unavailable"]
    )

    if st.button("Add Service"):
        data = {
            "service_name": service_name,
            "price": price,
            "description": description,
            "service_status": service_status
        }

        response = create_service(data)

        if response:
            st.success("Service added successfully")

    st.subheader("All Services")

    services = get_services()

    if services:
        st.dataframe(services)
    else:
        st.info("No services found")