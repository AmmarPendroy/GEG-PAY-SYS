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

    df = get_all_payments()
    if df.empty:
        st.info("No payment data found.")
        return

    role = user["role"]
    if role not in ["hq_pd", "hq_admin", "hq_accountant", "super_admin"]:
        df = df[df["project"] == user["project"]]

    st.subheader("Total Requests by Status")
    status_count = df["status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]
    st.dataframe(status_count)

    fig = px.pie(status_count, names="Status", values="Count", title="Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Requests by Contractor")
    contractor_count = df["contractor"].value_counts().reset_index()
    contractor_count.columns = ["Contractor", "Requests"]
    st.bar_chart(contractor_count.set_index("Contractor"))

    st.subheader("Payments Over Time")
    df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    df["month"] = df["submitted_at"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["amount"].sum().reset_index()
    st.line_chart(monthly.set_index("month"))
