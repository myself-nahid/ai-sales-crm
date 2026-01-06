import pandas as pd
from app.models.lead import Lead

def load_leads(csv_path: str) -> list[Lead]:
    df = pd.read_csv(csv_path)
    return [Lead(**row) for row in df.to_dict(orient="records")]

def save_leads(leads: list[Lead], output_path: str):
    df = pd.DataFrame([l.dict() for l in leads])
    df.to_csv(output_path, index=False)