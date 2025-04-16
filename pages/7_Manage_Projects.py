import streamlit as st
import pandas as pd
import os
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
    new_project = st.text_input("Project Name")
    if st.button("Add Project"):
        if new_project.strip() == "":
            st.warning("Please enter a valid name.")
        elif new_project in projects["name"].values:
            st.warning("Project already exists.")
        else:
            projects = pd.concat([projects, pd.DataFrame([{"name": new_project}])], ignore_index=True)
            save_projects(projects)
            st.success("Project added!")
            st.experimental_rerun()
