from fastapi import FastAPI
from app.pipelines.campaign_pipeline import run_campaign

app = FastAPI(title="AI Sales CRM")

@app.post("/run-campaign")
def run():
    return run_campaign()