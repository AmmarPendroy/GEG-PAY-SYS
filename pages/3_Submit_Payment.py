import streamlit as st
from modules.payments import submit_payment
from modules.auth import get_current_user

def show():
    st.title("📤 Submit Payment Request")
    
    user = get_current_user()
    if not user:
        st.warning("Please log in first.")
        return
    
    st.markdown(f"**Submitting for project:** `{user['project']}`")
    
    contractor = st.text_input("Contractor Name")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    work_period = st.date_input("Work Period")
    description = st.text_area("Description of Work")

    if st.button("Submit"):
        if all([contractor, amount, work_period, description]):
            data = {
                "contractor": contractor,
                "amount": amount,
                "work_period": str(work_period),
                "description": description,
                "submitted_by": user["email"],
                "project": user["project"]
            }
            submit_payment(data)
            st.success("Payment request submitted.")
        else:
            st.warning("All fields are required.")
