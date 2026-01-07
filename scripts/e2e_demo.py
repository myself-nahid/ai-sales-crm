import os
import subprocess
import time
import requests
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'


def run(cmd, cwd=ROOT):
    print('RUN:', cmd)
    subprocess.check_call(cmd, cwd=cwd, shell=True)


def wait_for(url, timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=3)
            return True
        except Exception:
            time.sleep(1)
    return False


if __name__ == '__main__':
    print('Starting e2e demo...')
    run('docker-compose up -d --build ollama mailhog api')

    print('Waiting for Ollama...')
    if not wait_for('http://localhost:11434'):
        print('Ollama did not start in time')
        exit(1)

    print('Waiting for API...')
    if not wait_for('http://localhost:8000'):
        print('API did not start in time')
        exit(1)

    # Trigger campaign
    print('Triggering campaign via API...')
    try:
        r = requests.post('http://localhost:8000/run-campaign', timeout=10)
        print('Trigger response:', r.status_code, r.text)
    except Exception as e:
        print('Failed to trigger:', e)
        exit(1)

    # Wait for enriched CSV
    enriched = DATA / 'enriched_leads.csv'
    deadline = time.time() + 120
    while time.time() < deadline:
        if enriched.exists():
            break
        time.sleep(1)

    if not enriched.exists():
        print('enriched_leads.csv not produced')
        exit(1)

    # Validate row count
    with open(enriched, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    count = len(rows) - 1
    print('Enriched rows:', count)
    if count < 20:
        print('FAIL: fewer than 20 leads processed')
        exit(1)

    # Check reports
    reports = list(REPORTS.glob('campaign_summary_*.md'))
    print('Reports found:', len(reports))
    if not reports:
        print('FAIL: no report generated')
        exit(1)

    print('E2E demo succeeded')
    print('Open MailHog at http://localhost:8025 to view messages')