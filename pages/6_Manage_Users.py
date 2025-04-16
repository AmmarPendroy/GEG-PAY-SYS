import streamlit as st
import pandas as pd
from modules.auth import get_current_user
from modules.users import load_users, save_users

def show():
    st.title("👥 Manage Users")
    user = get_current_user()
    if not user or user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied.")
        return

    users = load_users()
    pending = users[users["status"] == "pending"]

    st.subheader("Pending Users")
    if pending.empty:
        st.info("No pending users.")
    else:
        for idx, row in pending.iterrows():
            with st.expander(f"{row['name']} ({row['email']}) – {row['role']} – {row['project']}"):
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve", key=f"approve_{idx}"):
                    users.at[idx, "status"] = "approved"
                    save_users(users)
                    st.success(f"Approved {row['email']}")
                    st.experimental_rerun()
                if col2.button("❌ Reject", key=f"reject_{idx}"):
                    users.at[idx, "status"] = "rejected"
                    save_users(users)
                    st.warning(f"Rejected {row['email']}")
                    st.experimental_rerun()

    st.subheader("All Users")
    st.dataframe(users)
