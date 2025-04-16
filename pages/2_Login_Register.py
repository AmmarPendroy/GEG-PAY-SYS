import streamlit as st
import pandas as pd
import os
from modules.auth import login_user, register_user

PROJECTS_CSV = "data/projects.csv"

def load_projects():
    if not os.path.exists(PROJECTS_CSV):
        return ["ZAS4"]
    df = pd.read_csv(PROJECTS_CSV)
    return df["name"].tolist() if "name" in df.columns else ["ZAS4"]

def show_login_form():
    st.subheader("🔐 Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pw")
    if st.button("Login"):
        login_user(email, password)

def show_registration_form():
    st.subheader("📝 Register")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    is_hq = st.selectbox("Are you part of HQ or Site team?", ["HQ", "Site"])
    
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

def show():
    st.title("GEG Contractor Payment System")
    st.write("Welcome. Please log in or register below.")
    
    col1, col2 = st.columns(2)
    with col1:
        show_login_form()
    with col2:
        show_registration_form()
