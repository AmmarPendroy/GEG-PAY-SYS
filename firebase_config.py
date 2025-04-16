import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, db

# Load Admin SDK credentials
cred = credentials.Certificate("geg-pay-sys-firebase-adminsdk-fbsvc-949f2a165b.json")

# Initialize Firebase app once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": st.secrets["firebase"]["database_url"]
    })
