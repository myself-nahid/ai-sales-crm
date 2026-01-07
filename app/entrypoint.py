import os
import time
import requests
import sys
import os

root = os.getcwd()
if root not in sys.path:
    sys.path.insert(0, root)


def wait_for_service(url, timeout=60, interval=2):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False


def main():
    AUTO_RUN = os.getenv("AUTO_RUN", "true").lower() in ("1", "true", "yes")
    OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

    if AUTO_RUN:
        print(f"Waiting for Ollama at {OLLAMA_BASE}...")
        wait_for_service(OLLAMA_BASE, timeout=120)

        try:
            from app.pipelines.campaign_pipeline import run_campaign
            print("AUTO_RUN is enabled — running campaign...")
            run_campaign()
        except Exception as e:
            print(f"AUTO_RUN campaign failed: {e}")

    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)


if __name__ == '__main__':
    main()
