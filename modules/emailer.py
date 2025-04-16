import smtplib
import os
from email.message import EmailMessage
import streamlit as st

def send_email_with_attachment(to_email, subject, body, attachment_path):
    try:
        msg = EmailMessage()
        msg["From"] = st.secrets["email"]["sender"]
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)

        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(st.secrets["email"]["sender"], st.secrets["email"]["password"])
            smtp.send_message(msg)

    except Exception as e:
        st.warning(f"Email failed: {e}")
