from firebase_admin import db
from datetime import datetime

def submit_payment(data):
    data["submitted_at"] = datetime.utcnow().isoformat()
    data["status"] = "pending"
    db.reference("payments").push(data)

def get_all_payments():
    payments = db.reference("payments").get()
    if not payments:
        return []
    return [{**data, "id": pid} for pid, data in payments.items()]

def get_payments_by_user(email):
    return [p for p in get_all_payments() if p.get("submitted_by") == email]

def get_payments_by_project(project):
    return [p for p in get_all_payments() if p.get("project") == project]

def update_payment_status(payment_id, new_status):
    ref = db.reference(f"payments/{payment_id}")
    ref.update({"status": new_status})
