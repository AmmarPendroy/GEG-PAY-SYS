import pandas as pd
import os
from datetime import datetime

PAYMENTS_CSV = "data/payments.csv"

def load_payments():
    if not os.path.exists(PAYMENTS_CSV):
        return pd.DataFrame(columns=[
            "contractor", "amount", "work_period", "description",
            "submitted_by", "project", "status", "submitted_at"
        ])
    return pd.read_csv(PAYMENTS_CSV)

def save_payments(df):
    df.to_csv(PAYMENTS_CSV, index=False)

def submit_payment(data):
    df = load_payments()
    data["submitted_at"] = datetime.utcnow().isoformat()
    data["status"] = "pending"
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_payments(df)

def get_payments_by_user(email):
    df = load_payments()
    return df[df["submitted_by"] == email]

def get_payments_by_project(project):
    df = load_payments()
    return df[df["project"] == project]

def get_all_payments():
    return load_payments()

def update_payment_status(index, new_status):
    df = load_payments()
    if 0 <= index < len(df):
        df.at[index, "status"] = new_status
        save_payments(df)
