from firebase_config import db
from datetime import datetime

def submit_payment(data):
    timestamp = datetime.utcnow().isoformat()
    data['submitted_at'] = timestamp
    data['status'] = 'pending'
    db.child("payments").push(data)

def get_user_payments(email):
    all_payments = db.child("payments").get().val() or {}
    return [
        {**v, "id": k}
        for k, v in all_payments.items()
        if v.get("email") == email
    ]

def get_all_payments():
    all_payments = db.child("payments").get().val() or {}
    return [{**v, "id": k} for k, v in all_payments.items()]
