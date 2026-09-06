import streamlit as st

from frontend.api import get_dashboard

def show_dashboard():

    st.title("📊 Dashboard")

    data = get_dashboard()

    if "error" in data:
        st.error(data["error"])
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Customers",
            data["total_customers"]
        )

    with col2:
        st.metric(
            "🛏️ Rooms",
            data["total_rooms"]
        )

    with col3:
        st.metric(
            "📅 Bookings",
            data["total_bookings"]
        )

    with col4:
        st.metric(
            "💰 Revenue",
            f"₹{data['total_revenue']:,.2f}"
        )

    st.divider()

    st.info(
        "Dashboard statistics are loaded dynamically "
        "from the FastAPI backend."
    )