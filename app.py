import streamlit as st
from pages import login, register, submit, review, myrequests, adminusers, reports
from modules.auth import get_current_user, logout_user

st.set_page_config(page_title="GEG Contractor Payment", layout="wide")

def show_sidebar():
    user = get_current_user()
    if user:
        st.sidebar.markdown(f"**Logged in as:** {user['email']}")
        st.sidebar.markdown(f"**Role:** {user['role'].title()}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.experimental_rerun()
    else:
        st.sidebar.markdown("**Please log in**")

def main():
    user = get_current_user()
    show_sidebar()

    if not user:
        page = st.sidebar.selectbox("Select Page", ["Login", "Register"])
        if page == "Login":
            login.show()
        else:
            register.show()
        return

    role = user.get("role", "")
    page = st.sidebar.selectbox("Select Page", [
        "Submit Payment",
        "My Requests",
        "Review Requests" if role in ["hq_admin", "hq_director", "zas_pm", "zas_accountant"] else None,
        "Admin Users" if role in ["hq_admin", "hq_director"] else None,
        "Reports"
    ])

    if page == "Submit Payment":
        submit.show()
    elif page == "My Requests":
        myrequests.show()
    elif page == "Review Requests":
        review.show()
    elif page == "Admin Users":
        adminusers.show()
    elif page == "Reports":
        reports.show()

if __name__ == "__main__":
    main()
