import pandas as pd
import os

USERS_CSV = "data/users.csv"

def load_users():
    if not os.path.exists(USERS_CSV):
        return pd.DataFrame(columns=["email", "name", "role", "project", "status"])
    return pd.read_csv(USERS_CSV)

def save_users(df):
    df.to_csv(USERS_CSV, index=False)
