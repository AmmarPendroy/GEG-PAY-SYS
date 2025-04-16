import streamlit as st
import pandas as pd
from modules.auth import get_current_user
from modules.payments import get_all_payments
from modules.projects import load_projects
import plotly.express as px

def show():
    st.title("📍 Charts by Site Location")

    user = get_current_user()
    if not user:
        st.warning("Please log in.")
        return

    if user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied.")
        return

    df = get_all_payments()
    projects_df = load_projects()

    if df.empty or projects_df.empty:
        st.info("No data to show.")
        return

    merged = pd.merge(df, projects_df, how="left", on="name" if "name" in projects_df.columns else "project")
    grouped = merged.groupby("location")["amount"].sum().reset_index()

    st.subheader("Total Approved Payment Amount by Location")
    st.plotly_chart(px.bar(grouped, x="location", y="amount", title="Payments by Site Location"), use_container_width=True)
