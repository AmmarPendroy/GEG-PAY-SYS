import streamlit as st
from modules.auth import login_user, auto_super_admin_login

def show():
    st.title("Login")
    auto_super_admin_login()

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success("Login successful!")
            st.experimental_rerun()
