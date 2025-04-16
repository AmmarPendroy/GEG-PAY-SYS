import streamlit as st
from modules.auth import register_user

def show():
    st.title("Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", [
        "contractor", "hq_admin", "hq_director",
        "hq_accountant", "zas_pm", "zas_accountant"
    ])

    if st.button("Register"):
        if name and email and password and role:
            register_user(name, email, password, role)
        else:
            st.warning("Please fill out all fields.")
