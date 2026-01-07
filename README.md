# AI-Enhanced Sales Campaign CRM (MVP)

An end-to-end **AI-powered sales outreach MVP** that automates lead enrichment, prioritization, personalized email drafting, response classification, and campaign reporting — all running **locally** using a self-hosted LLM (**Ollama**) and fully containerized with Docker.

This project demonstrates a complete, production-style AI pipeline for sales automation with **one-command execution**.

---

## Project Overview

The system ingests a CSV of leads, processes them through an AI-driven pipeline, sends personalized outreach emails to a local SMTP server (MailHog), simulates email responses, and generates both enriched lead data and a final campaign summary report.

This MVP is designed to showcase:
- Practical AI usage in backend systems
- Local LLM orchestration without third-party APIs
- A clean, demo-first engineering approach

---

## Tech Stack

### Backend
- Python 3.10
- FastAPI
- Pandas
- Pydantic

### AI / LLM
- Ollama (local LLM runtime)
- Model: `llama3.2:3b`

### Infrastructure
- Docker
- Docker Compose

### Email Testing
- MailHog (local SMTP server + web UI)

---

## Core Features & Acceptance Criteria

### 1. Lead Ingestion
- Reads an initial list of leads from `data/leads.csv`
- Supports **20+ leads** per campaign run

---

### 2. AI-Powered Enrichment & Scoring (via Ollama)
- Scores and prioritizes each lead as **High**, **Medium**, or **Low**
- Suggests a buyer persona (e.g., *Technical Decision Maker*)
- Generates a **unique, short, and personalized outreach email** for every lead
- Automatically classifies simulated email responses into:
  - **Interested**
  - **Not Interested**
  - **Follow Up**

---

### 3. Automated Outreach
- Sends generated emails via SMTP
- Uses **MailHog** to safely intercept all outgoing emails
- Enables local inspection of emails without sending real messages

---

### 4. Data Write-Back & Reporting
- Writes AI-enriched results to `data/enriched_leads.csv`
- Generates a final **AI-written campaign summary report** in Markdown format
- Includes campaign statistics and high-level insights

---

### 5. Demo-First & Docker Ready
- Entire application stack runs with a **single command**
- Pipeline executes automatically on startup
- Fully reproducible local environment

---

## System Architecture

The application runs as a set of interconnected Docker containers.

### Services

#### `api`
- FastAPI-based backend
- Orchestrates the entire sales campaign pipeline
- Handles lead ingestion, AI prompts, email sending, response classification, and reporting
- Automatically runs the campaign on startup

#### `ollama`
- Hosts the local Large Language Model
- Processes enrichment, scoring, email generation, and classification prompts
- Communicates with the `api` service over HTTP

#### `mailhog`
- Local SMTP server for testing
- Captures all outgoing emails
- Provides a web interface to view emails in real time

---

### High-Level Flow
```
leads.csv
↓
FastAPI Campaign Pipeline
↓
Ollama (LLM Processing)
↓
MailHog (Email Capture)
↓
enriched_leads.csv
↓
campaign_summary.md
```

## Launch the Application
```
docker compose up --build
```