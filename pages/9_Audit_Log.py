import streamlit as st
import pandas as pd
import os
from modules.auth import get_current_user

AUDIT_CSV = "data/audit_log.csv"

def show():
    st.title("🧾 Audit Log Viewer")
    user = get_current_user()

    if not user or user["role"] not in ["hq_pd", "hq_admin", "super_admin"]:
        st.error("Access denied.")
        return

    if not os.path.exists(AUDIT_CSV):
        st.info("No audit logs yet.")
        return

    df = pd.read_csv(AUDIT_CSV)
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    with st.expander("Download Log"):
        st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="audit_log.csv")
