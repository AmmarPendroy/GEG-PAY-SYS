import streamlit as st
from firebase_config import auth, db

SUPER_ADMIN = {
    "email": "ammar.muhammed@geg-construction.com",
    "password": "AmmarGEG99$",
    "role": "super_admin",
    "status": "approved",
    "name": "Ammar Muhammad"
}

def login_user(email, password):
    if not email.endswith("@geg-construction.com"):
        st.error("Only @geg-construction.com emails are allowed.")
        return None

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        profile = db.child("users").child(uid).get().val()
        if not profile:
            st.error("User profile not found.")
            return None

        if profile.get("status") != "approved":
            st.warning("Your account is not yet approved.")
            return None

        st.session_state.user = {
            "uid": uid,
            "email": email,
            "role": profile.get("role", "contractor"),
            "name": profile.get("name", "")
        }
        return st.session_state.user
    except:
        st.error("Login failed. Check credentials.")
        return None

def register_user(name, email, password, role):
    if not email.endswith("@geg-construction.com"):
        st.error("Only @geg-construction.com emails are allowed.")
        return

    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        db.child("users").child(uid).set({
            "email": email,
            "name": name,
            "role": role,
            "status": "pending"
        })
        st.success("Registration submitted! Wait for approval.")
    except:
        st.error("Registration failed. Email might be used already.")

def get_current_user():
    return st.session_state.get("user", None)

def logout_user():
    st.session_state.user = None

def auto_super_admin_login():
    if SUPER_ADMIN["email"] not in st.session_state:
        try:
            user = auth.sign_in_with_email_and_password(
                SUPER_ADMIN["email"], SUPER_ADMIN["password"]
            )
            st.session_state.user = {
                "uid": user["localId"],
                "email": SUPER_ADMIN["email"],
                "role": SUPER_ADMIN["role"],
                "name": SUPER_ADMIN["name"]
            }
        except:
            pass
