
import streamlit as st
from firebase_config import auth, db  ✅

SUPER_ADMIN_EMAIL = "ammar.muhammed@geg-construction.com"
SUPER_ADMIN_PASSWORD = "AmmarGEG99$"

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    st.session_state.user = None

def auto_login_super_admin():
    if "user" not in st.session_state:
        st.session_state.user = {
            "email": SUPER_ADMIN_EMAIL,
            "role": "super_admin",
            "name": "Super Admin",
            "project": "All"
        }

def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        uid = user.uid
        profile = db.reference(f"users/{uid}").get()

        if not profile:
            st.error("User profile not found.")
            return

        if profile.get("status") != "approved":
            st.warning("Your account is not yet approved.")
            return

        if profile.get("password") != password:
            st.error("Incorrect password.")
            return

        st.session_state.user = {
            "uid": uid,
            "email": email,
            "role": profile.get("role", "contractor"),
            "name": profile.get("name", ""),
            "project": profile.get("project", "")
        }
        st.success("Login successful!")
        st.experimental_rerun()

    except Exception as e:
        st.error("Login failed. Check your email and password.")

def register_user(name, email, password, role, project, is_hq):
    st.toast("📝 Registration submitted. Awaiting approval.")
    try:
        user = auth.create_user(email=email, password=password)
        uid = user.uid
        profile_data = {
            "email": email,
            "name": name,
            "role": role,
            "project": project,
            "status": "pending",
            "password": password,
            "team": is_hq
        }
        db.reference(f"users/{uid}").set(profile_data)
        st.success("Registration submitted! Await approval.")
    except Exception as e:
        st.error("Registration failed. Email may already be in use.")

