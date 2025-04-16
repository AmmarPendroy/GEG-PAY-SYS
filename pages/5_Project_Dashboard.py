import streamlit as st
import pandas as pd
from modules.auth import get_current_user
from modules.payments import get_all_payments
import plotly.express as px

def show():
    st.title("📊 Project Dashboard")
    user = get_current_user()

    if not user:
        st.warning("Please log in.")
        return

    all_data = get_all_payments()
    if not all_data:
        st.info("No payment data available.")
        return

    df = pd.DataFrame(all_data)
    if user["role"] not in ["hq_pd", "hq_admin", "hq_accountant", "super_admin"]:
        df = df[df["project"] == user["project"]]

    if df.empty:
        st.info("No data for your project.")
        return

    # Status Pie Chart
    st.subheader("Status Distribution")
    status_count = df["status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]
    st.plotly_chart(px.pie(status_count, names="Status", values="Count"), use_container_width=True)

    # Contractor Chart
    st.subheader("Requests by Contractor")
    contractor_count = df["contractor"].value_counts().reset_index()
    contractor_count.columns = ["Contractor", "Requests"]
    st.bar_chart(contractor_count.set_index("Contractor"))

    # Payments Over Time
    st.subheader("Payments Over Time")
    df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    df["month"] = df["submitted_at"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["amount"].sum().reset_index()
    st.line_chart(monthly.set_index("month"))
