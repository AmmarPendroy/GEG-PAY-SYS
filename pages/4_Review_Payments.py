import streamlit as st
import pandas as pd
from modules.auth import get_current_user
from modules.payments import get_all_payments, update_payment_status

def show():
    st.title("🧾 Review Submitted Payments")
    user = get_current_user()
    if not user:
        st.warning("Please log in.")
        return

    if user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied. HQ access only.")
        return

    payments = get_all_payments()
    if payments.empty:
        st.info("No payments found.")
        return

    project_filter = st.selectbox("Filter by Project", options=["All"] + sorted(payments["project"].unique().tolist()))
    
    if project_filter != "All":
        payments = payments[payments["project"] == project_filter]

    st.write(f"Showing {len(payments)} records.")
    for i, row in payments.iterrows():
        with st.expander(f"{row['contractor']} – {row['amount']} USD – {row['status'].upper()}"):
            st.write(f"**Project:** {row['project']}")
            st.write(f"**Work Period:** {row['work_period']}")
            st.write(f"**Submitted By:** {row['submitted_by']}")
            st.write(f"**Description:**\n{row['description']}")
            st.write(f"**Submitted At:** {row['submitted_at']}")

            if row["status"] == "pending":
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve", key=f"approve_{i}"):
                    update_payment_status(i, "approved")
                    st.success("Approved!")
                    st.experimental_rerun()
                if col2.button("❌ Reject", key=f"reject_{i}"):
                    update_payment_status(i, "rejected")
                    st.warning("Rejected.")
                    st.experimental_rerun()
