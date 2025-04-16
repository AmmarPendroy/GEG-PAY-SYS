from firebase_admin import db
from datetime import datetime

def log_action(user_email, action, payment_data, filename=""):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_email,
        "action": action,
        "contractor": payment_data.get("contractor", ""),
        "project": payment_data.get("project", ""),
        "amount": payment_data.get("amount", ""),
        "filename": filename
    }
    db.reference("audit").push(entry)

def get_all_audit_logs():
    data = db.reference("audit").get()
    if not data:
        return []
    return list(data.values())
