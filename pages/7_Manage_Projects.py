import streamlit as st
from modules.auth import get_current_user
from modules.projects import get_all_project_dicts, add_project

def show():
    st.title("🏗️ Manage Projects")
    user = get_current_user()
    if not user or user["role"] != "hq_pd":
        st.error("Access restricted to HQ Project Director.")
        return

    st.subheader("Existing Projects")
    projects = get_all_project_dicts()
    if projects:
        st.table(projects)
    else:
        st.info("No projects found.")

    st.subheader("Add New Project")
    name = st.text_input("Project Name")
    location = st.text_input("Location")
    remark = st.text_area("Remark")

    if st.button("Add Project"):
        if not name or not location:
            st.warning("Project name and location are required.")
        else:
            add_project(name, location, remark)
            st.success("Project added successfully.")
            st.experimental_rerun()
