# MindSync AI — Mental Health & Healthcare Assistant

An offline, AI-powered healthcare platform for mental health consultations, clinical report generation, symptom triage, and mood tracking. All AI inference runs locally — no cloud, no data leaves your machine.

---

## Features

- AI Consultation — Context-aware mental health conversations
- Clinical Report Generator — Auto-generates structured patient reports with risk levels
- Symptom Assessment — Triage with urgency classification (ROUTINE / SOON / URGENT / EMERGENCY)
- Mood Tracker — Log and review patient mood history
- Patient & Session Management — Full CRUD with UUID-based records
- Crisis Detection — Instantly shows helpline numbers for crisis keywords
- Domain Restricted — AI strictly stays within healthcare topics

---

## Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/) — check **"Add Python to PATH"** during install
- [Ollama](https://ollama.com) — local AI engine

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mindsync-ai.git
cd mindsync-ai
```

### 2. Pull the AI model

```bash
ollama pull llama3.2:1b
```

> Make sure Ollama is running in the background before starting the app.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**
```bash
.\.venv\Scripts\Activate.ps1
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

> On Windows, if you get an execution policy error run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 5. Install dependencies

```bash
pip install flask ollama
```

### 6. Run the app

```bash
python app.py
```

### 7. Open in browser

```
http://localhost:5000
```

---

## Project Structure

```
MindSync AI/
├── app.py                  # Flask backend — 14 API routes
├── chat.json               # Patient data storage (auto-created)
├── requirement.txt         # Python dependencies
├── generate_report.py      # Script to generate DOCX project report
├── templates/
│   └── index.html          # Frontend HTML
└── static/
    ├── css/
    │   └── styles.css      # Stylesheet
    └── js/
        └── app.js          # Frontend JavaScript
```

---

## API Endpoints

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/get_patients` | GET | Get all patients |
| `/add_patient` | POST | Create a patient |
| `/rename_patient` | POST | Rename a patient |
| `/delete_patient` | POST | Delete a patient |
| `/add_session` | POST | Create a session |
| `/rename_session` | POST | Rename a session |
| `/delete_session` | POST | Delete a session |
| `/chat` | POST | Send message, get AI response |
| `/generate_report` | POST | Generate clinical report |
| `/log_mood` | POST | Log a mood score |
| `/get_mood_logs` | POST | Get mood history |
| `/health_assessment` | POST | Symptom triage |
| `/export_patient` | POST | Export patient data as JSON |

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python + Flask |
| AI Engine | Ollama (local) |
| AI Model | llama3.2:1b |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Storage | JSON file |

---

## Crisis Support

If a patient mentions crisis keywords (e.g. "suicide", "self harm"), the app immediately bypasses the AI and displays:

- **iCall** — 9152987821
- **Vandrevala Foundation** — 1860-2662-345

---

## Disclaimer

MindSync AI is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.
