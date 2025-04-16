import streamlit as st
import pandas as pd
import os
from modules.auth import get_current_user

AUDIT_CSV = "data/audit_log.csv"

def show():
    st.title("🧾 Audit Log Viewer")
    user = get_current_user()

    if not user or user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied.")
        return

    if not os.path.exists(AUDIT_CSV):
        st.info("No audit logs yet.")
        return

    df = pd.read_csv(AUDIT_CSV, parse_dates=["timestamp"])

    st.subheader("🔎 Filter Logs")

    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=df["timestamp"].min().date())
    with col2:
        end_date = st.date_input("End Date", value=df["timestamp"].max().date())

    # Action filter
    action_filter = st.multiselect("Filter by Action", df["action"].unique().tolist(), default=df["action"].unique().tolist())

    # User email filter
    user_filter = st.text_input("Search by User Email (optional)")

    # Apply filters
    filtered = df[
        (df["timestamp"].dt.date >= start_date) &
        (df["timestamp"].dt.date <= end_date) &
        (df["action"].isin(action_filter))
    ]

    if user_filter:
        filtered = filtered[filtered["user"].str.contains(user_filter, case=False)]

    st.write(f"Showing {len(filtered)} entries")
    st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True)

    with st.expander("⬇️ Download Log"):
        st.download_button("📥 Download Filtered CSV", data=filtered.to_csv(index=False), file_name="filtered_audit_log.csv")
