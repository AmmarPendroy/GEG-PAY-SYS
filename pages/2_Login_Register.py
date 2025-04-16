import streamlit as st
from modules.auth import login_user, register_user
from modules.projects import load_projects

def show():
    st.title("GEG Contractor Payment System")
    st.write("Welcome. Please log in or register below.")

    col1, col2 = st.columns(2)
    
    # 🔐 LOGIN
    with col1:
        st.subheader("🔐 Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            login_user(email, password)

    # 📝 REGISTER
    with col2:
        st.subheader("📝 Register")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        is_hq = st.selectbox("Team", ["HQ", "Site"])

        if is_hq == "HQ":
            role = st.selectbox("Select Role", ["hq_pd", "hq_admin", "hq_accountant"])
        else:
            role = st.selectbox("Select Role", ["project_manager", "site_accountant"])

        project = st.selectbox("Select Project", load_projects())

        if st.button("Register"):
            if all([name, email, password, role, project]):
                register_user(name, email, password, role, project, is_hq)
            else:
                st.warning("Please complete all fields.")
