import streamlit as st
import pandas as pd
from modules.auth import get_current_user
from modules.projects import load_projects, save_projects

def show():
    st.title("🏗️ Manage Projects")
    user = get_current_user()
    if not user or user["role"] != "hq_pd":
        st.error("Access restricted to HQ Project Director.")
        return

    projects = load_projects()
    st.subheader("Existing Projects")
    st.dataframe(projects)

    st.subheader("Add New Project")
    name = st.text_input("Project Name")
    location = st.text_input("Location")
    remark = st.text_area("Remark")

    if st.button("Add Project"):
        if not name or not location:
            st.warning("Project name and location are required.")
        elif name in projects["name"].values:
            st.warning("Project already exists.")
        else:
            new_row = pd.DataFrame([{
                "name": name,
                "location": location,
                "remark": remark
            }])
            projects = pd.concat([projects, new_row], ignore_index=True)
            save_projects(projects)
            st.success("Project added!")
            st.experimental_rerun()
