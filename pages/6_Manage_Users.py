import streamlit as st
from modules.auth import get_current_user
from modules.users import get_all_users, get_pending_users, approve_user, reject_user

def show():
    st.title("👥 Manage Users")
    user = get_current_user()
    
    if not user or user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied.")
        return

    st.subheader("Pending Users")
    pending_users = get_pending_users()
    if not pending_users:
        st.info("No pending users.")
    else:
        for u in pending_users:
            with st.expander(f"{u['name']} | {u['email']} | {u['role']} | {u['project']}"):
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve", key=f"approve_{u['uid']}"):
                    approve_user(u['uid'])
                    st.success(f"Approved {u['email']}")
                    st.experimental_rerun()
                if col2.button("❌ Reject", key=f"reject_{u['uid']}"):
                    reject_user(u['uid'])
                    st.warning(f"Rejected {u['email']}")
                    st.experimental_rerun()

    st.subheader("All Users")
    all_users = get_all_users()
    st.dataframe([{k: v for k, v in user.items() if k != 'password'} for user in all_users])
