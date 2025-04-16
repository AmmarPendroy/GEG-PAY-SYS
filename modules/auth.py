import streamlit as st
from firebase_config import auth
import pandas as pd
import os

USERS_CSV = "data/users.csv"
SUPER_ADMIN_EMAIL = "ammar.muhammed@geg-construction.com"
SUPER_ADMIN_PASSWORD = "AmmarGEG99$"

def load_users():
    if not os.path.exists(USERS_CSV):
        return pd.DataFrame(columns=["email", "name", "role", "project", "status"])
    return pd.read_csv(USERS_CSV)

def save_users(df):
    df.to_csv(USERS_CSV, index=False)

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    st.session_state.user = None

def auto_login_super_admin():
    if "user" not in st.session_state and st.secrets.get("firebase"):
        try:
            user = auth.sign_in_with_email_and_password(SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD)
            st.session_state.user = {
                "email": SUPER_ADMIN_EMAIL,
                "role": "super_admin",
                "name": "Super Admin",
                "project": "All"
            }
        except:
            pass

def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        users_df = load_users()
        user_row = users_df[users_df["email"] == email]
        if user_row.empty:
            st.error("User not registered.")
            return
        if user_row.iloc[0]["status"] != "approved":
            st.warning("Your account is not yet approved.")
            return

        st.session_state.user = {
            "email": email,
            "role": user_row.iloc[0]["role"],
            "name": user_row.iloc[0]["name"],
            "project": user_row.iloc[0]["project"]
        }
        st.success("Login successful!")
        st.experimental_rerun()

    except:
        st.error("Login failed. Check credentials.")

def register_user(name, email, password, role, project, is_hq):
    try:
        auth.create_user_with_email_and_password(email, password)
        users_df = load_users()
        new_user = pd.DataFrame([{
            "email": email,
            "name": name,
            "role": role,
            "project": project,
            "status": "pending"
        }])
        updated_df = pd.concat([users_df, new_user], ignore_index=True)
        save_users(updated_df)
        st.success("Registration submitted! Please wait for approval.")
    except:
        st.error("Registration failed. Email might be already registered.")
