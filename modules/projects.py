import pandas as pd
import os

PROJECTS_CSV = "data/projects.csv"

def load_projects():
    if not os.path.exists(PROJECTS_CSV):
        return pd.DataFrame(columns=["name", "location", "remark"])
    return pd.read_csv(PROJECTS_CSV)

def save_projects(df):
    df.to_csv(PROJECTS_CSV, index=False)
