import streamlit as st

from modules.auth import get_current_user, logout_user, auto_login_super_admin


# Load user session or auto-login if super admin
auto_login_super_admin()

st.set_page_config(page_title="GEG Contractor Payment", layout="wide")
user = get_current_user()

# Sidebar
st.sidebar.image("assets/logo.png", use_column_width=True)
if user:
    st.sidebar.markdown(f"**Logged in as:** {user['email']}")
    st.sidebar.markdown(f"**Role:** {user['role'].upper()}")
    if st.sidebar.button("Logout"):
        logout_user()
        st.experimental_rerun()

# Pages by role
def show_menu():
    role = user["role"]

    menu = []

    if role in ["hq_pd", "hq_admin", "hq_accountant", "project_manager", "site_accountant"]:
        menu.append("Submit Payment")

    if role in ["hq_pd", "hq_admin", "hq_accountant", "project_manager", "site_accountant"]:
        menu.append("Project Dashboard")

    if role in ["hq_pd", "hq_admin"]:
        menu.append("Review Payments")
        menu.append("Manage Users")

    if role == "hq_pd":
        menu.append("Manage Projects")

    if role in ["hq_pd", "hq_admin", "super_admin"]:
        menu.append("Site Charts")
        menu.append("Audit Log")

    menu.append("Help Guide")

    return st.sidebar.radio("Navigate", menu)

if not user:
    st.switch_page("pages/2_Login_Register.py")
else:
    page = show_menu()

    if page == "Submit Payment":
        st.switch_page("pages/3_Submit_Payment.py")
    elif page == "Project Dashboard":
        st.switch_page("pages/5_Project_Dashboard.py")
    elif page == "Review Payments":
        st.switch_page("pages/4_Review_Payments.py")
    elif page == "Manage Users":
        st.switch_page("pages/6_Manage_Users.py")
    elif page == "Manage Projects":
        st.switch_page("pages/7_Manage_Projects.py")
    elif page == "Site Charts":
        st.switch_page("pages/8_Site_Charts.py")
    elif page == "Audit Log":
        st.switch_page("pages/9_Audit_Log.py")
    elif page == "Help Guide":
        st.switch_page("pages/1_Help_guide.py")
