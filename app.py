import streamlit as st
from pages import submit, review, myrequests, adminusers, reports

st.set_page_config(page_title="GEG Contractor Payment", layout="wide")

def main():
    st.sidebar.image("assets/logo.png", use_column_width=True)
    st.sidebar.title("Navigation")
    
    page = st.sidebar.selectbox("Select Page", [
        "Submit Payment",
        "My Requests",
        "Review Requests",
        "Admin Users",
        "Reports"
    ])

    if page == "Submit Payment":
        submit.show()
    elif page == "My Requests":
        myrequests.show()
    elif page == "Review Requests":
        review.show()
    elif page == "Admin Users":
        adminusers.show()
    elif page == "Reports":
        reports.show()

if __name__ == "__main__":
    main()
