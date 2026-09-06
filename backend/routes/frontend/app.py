import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🏨",
    layout="wide"
)

# =========================================================
# IMPORTS
# =========================================================

from frontend.api import login
from frontend.pages.dashboard import show_dashboard
from frontend.pages.customers import show_customers
from frontend.pages.rooms import show_rooms
from frontend.pages.bookings import show_bookings
from frontend.pages.payments import show_payments
from frontend.pages.services import show_services
from frontend.pages.reports import show_reports


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.title("🏨 Hotel Management System")
    st.subheader("Login")

    with st.form("login_form"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button("Login")

        if submitted:

            if not username or not password:
                st.error("Please enter username and password.")
                return

            result = login(username, password)

            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.logged_in = True
                st.session_state.username = result.get(
                    "username",
                    username
                )

                st.success("Login successful!")
                st.rerun()


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    if not st.session_state.logged_in:
        login_page()
        return

    st.sidebar.title("🏨 Hotel Management")

    st.sidebar.write(
        f"Welcome, **{st.session_state.username}**"
    )

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Customers",
            "Rooms",
            "Bookings",
            "Payments",
            "Services",
            "Reports",
            "Logout"
        ]
    )

    if page == "Dashboard":
        show_dashboard()

    elif page == "Customers":
        show_customers()

    elif page == "Rooms":
        show_rooms()

    elif page == "Bookings":
        show_bookings()

    elif page == "Payments":
        show_payments()

    elif page == "Services":
        show_services()

    elif page == "Reports":
        show_reports()

    elif page == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    main()