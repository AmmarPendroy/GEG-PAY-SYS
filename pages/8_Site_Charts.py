import streamlit as st
import pandas as pd
from modules.auth import get_current_user
from modules.payments import get_all_payments
from modules.projects import get_all_project_dicts
import plotly.express as px

def show():
    st.title("📍 Site Charts by Location")
    user = get_current_user()

    if not user or user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access restricted to HQ team.")
        return

    payments = get_all_payments()
    projects = get_all_project_dicts()

    if not payments or not projects:
        st.info("No data available.")
        return

    df_payments = pd.DataFrame(payments)
    df_projects = pd.DataFrame(projects)

    # Merge payments with project location
    merged = pd.merge(df_payments, df_projects, on="name" if "name" in df_projects.columns else "project")

    # Aggregate by location
    grouped = merged.groupby("location")["amount"].sum().reset_index()

    st.subheader("Total Payment Amount by Location")
    st.plotly_chart(
        px.bar(grouped, x="location", y="amount", title="Payments by Site Location"),
        use_container_width=True
    )
