import streamlit as st
import pandas as pd
from datetime import datetime
from modules.auth import get_current_user
from modules.audit import get_all_audit_logs

def show():
    st.title("🧾 Audit Log Viewer")
    user = get_current_user()

    if not user or user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied.")
        return

    logs = get_all_audit_logs()
    if not logs:
        st.info("No audit logs found.")
        return

    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.subheader("🔎 Filter Logs")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=df["timestamp"].min().date())
    with col2:
        end_date = st.date_input("End Date", value=df["timestamp"].max().date())

    action_filter = st.multiselect("Action", df["action"].unique(), default=df["action"].unique())
    user_filter = st.text_input("Filter by Email")

    filtered = df[
        (df["timestamp"].dt.date >= start_date) &
        (df["timestamp"].dt.date <= end_date) &
        (df["action"].isin(action_filter))
    ]

    if user_filter:
        filtered = filtered[filtered["user"].str.contains(user_filter, case=False)]

    st.write(f"Showing {len(filtered)} logs")
    st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True)

    with st.expander("⬇️ Download"):
        st.download_button("📥 Download CSV", filtered.to_csv(index=False), "audit_log_filtered.csv")
