import pandas as pd
import os
from datetime import datetime

AUDIT_LOG = "data/audit_log.csv"

def log_action(user_email, action, payment_data, filename=""):
    os.makedirs("data", exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_email,
        "action": action,
        "contractor": payment_data.get("contractor", ""),
        "project": payment_data.get("project", ""),
        "amount": payment_data.get("amount", ""),
        "filename": filename
    }

    if os.path.exists(AUDIT_LOG):
        df = pd.read_csv(AUDIT_LOG)
    else:
        df = pd.DataFrame(columns=entry.keys())

    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(AUDIT_LOG, index=False)
