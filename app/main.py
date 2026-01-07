from fastapi import FastAPI, BackgroundTasks
from app.pipelines.campaign_pipeline import run_campaign

app = FastAPI(title="AI Sales CRM")

@app.post("/run-campaign")
def run(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_campaign)
    return {"status": "Campaign started in background"}

@app.get("/")
def health():
    return {"status": "AI Sales CRM is running", "message": "Use POST /run-campaign to start"}