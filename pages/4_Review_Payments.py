import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

from modules.auth import get_current_user
from modules.payments import get_all_payments, update_payment_status
from modules.audit import log_action
from modules.emailer import send_email_with_attachment

EXPORT_DIR = "exports"
os.makedirs("exports", exist_ok=True)

def generate_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.output(os.path.join(EXPORT_DIR, filename))

def show():
    st.title("🧾 Review Submitted Payments")
    user = get_current_user()
    if not user:
        st.warning("Please log in.")
        return

    if user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied. HQ access only.")
        return

    payments = get_all_payments()
    if not payments:
        st.info("No payments found.")
        return

    project_filter = st.selectbox("Filter by Project", options=["All"] + sorted(set(p["project"] for p in payments)))
    filtered = [p for p in payments if p["project"] == project_filter] if project_filter != "All" else payments

    for i, row in enumerate(filtered):
        with st.expander(f"{row['contractor']} – {row['amount']} USD – {row['status'].upper()}"):
            st.write(f"**Project:** {row['project']}")
            st.write(f"**Work Period:** {row['work_period']}")
            st.write(f"**Submitted By:** {row['submitted_by']}")
            st.write(f"**Description:**\n{row['description']}")
            st.write(f"**Submitted At:** {row['submitted_at']}")

            filename = f"{row['project']}_{row['contractor']}_{i}.pdf"
            filepath = os.path.join(EXPORT_DIR, filename)

            if row["status"] == "pending":
                col1, col2 = st.columns(2)

                if col1.button("✅ Approve", key=f"approve_{i}"):
                    update_payment_status(row["id"], "approved")
                    generate_pdf(row, filename)
                    log_action(user["email"], "approved", row, filename)
                    send_email_with_attachment(
                        user["email"],
                        "Payment Approved",
                        f"Payment for {row['contractor']} has been approved.",
                        filepath
                    )
                    st.success(f"Approved and saved as {filename}")
                    st.toast("✅ Payment approved and PDF saved.")
                    st.experimental_rerun()

                if col2.button("❌ Reject", key=f"reject_{i}"):
                    update_payment_status(row["id"], "rejected")
                    log_action(user["email"], "rejected", row)
                    st.warning("Rejected.")
                    st.toast("❌ Payment rejected.")
                    st.experimental_rerun()

            if row["status"] == "approved":
                try:
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="📄 Download PDF",
                            data=f.read(),
                            file_name=filename,
                            mime="application/pdf",
                            key=f"dl_{i}"
                        )
                except FileNotFoundError:
                    st.warning("⚠️ PDF file not found.")
