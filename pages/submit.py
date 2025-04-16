import streamlit as st
from modules.payments import submit_payment

def show():
    st.title("Submit Payment Request")

    name = st.text_input("Contractor Name")
    email = st.text_input("Email")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    work_period = st.date_input("Work Period")
    description = st.text_area("Work Description")
    doc_link = st.text_input("Document Link (optional)")

    if st.button("Submit Request"):
        if name and email and amount and work_period and description:
            payment_data = {
                "name": name,
                "email": email,
                "amount": amount,
                "work_period": str(work_period),
                "description": description,
                "doc_link": doc_link,
            }
            submit_payment(payment_data)
            st.success("Payment request submitted!")
        else:
            st.warning("Please fill all required fields.")
