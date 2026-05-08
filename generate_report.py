"""
Generate Project Report for MindSync AI as a DOCX file
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
import os


doc = Document()

# ==================== STYLES ====================
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(12)
font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

style = doc.styles['Heading 1']
font = style.font
font.name = 'Calibri'
font.size = Pt(22)
font.bold = True
font.color.rgb = RGBColor(0x00, 0x2B, 0x5C)

style = doc.styles['Heading 2']
font = style.font
font.name = 'Calibri'
font.size = Pt(16)
font.bold = True
font.color.rgb = RGBColor(0x1A, 0x47, 0x8A)

style = doc.styles['Heading 3']
font = style.font
font.name = 'Calibri'
font.size = Pt(14)
font.bold = True
font.color.rgb = RGBColor(0x1A, 0x47, 0x8A)

SRM_BLUE = RGBColor(0x00, 0x2B, 0x5C)
SRM_GOLD = RGBColor(0xC8, 0x96, 0x2E)
DARK = RGBColor(0x1A, 0x1A, 0x2E)
GRAY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def add_centered(text, size=12, bold=False, color=DARK, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = 'Calibri'
    return p


def add_para(text, size=12, bold=False, color=DARK, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = 'Calibri'
    return p


def add_bullet(text, size=11, color=DARK):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.clear()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.name = 'Calibri'
    return p


def add_numbered(text, size=11, color=DARK):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.space_after = Pt(4)
    p.clear()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.name = 'Calibri'
    return p


def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11)
                run.font.name = 'Calibri'

    # Data
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
                    run.font.name = 'Calibri'

    doc.add_paragraph()
    return table


def add_hr():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run('_' * 80)
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)


def page_break():
    doc.add_page_break()


# =====================================================
# TITLE PAGE
# =====================================================

doc.add_paragraph()
doc.add_paragraph()
add_centered("SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", 18, True, SRM_BLUE)
add_centered("(Deemed to be University u/s 3 of UGC Act, 1956)", 11, False, GRAY)
add_centered("Kattankulathur — 603203, Chengalpattu District, Tamil Nadu", 11, False, GRAY)
doc.add_paragraph()
add_centered("Department of Computer Science and Engineering", 14, True, SRM_BLUE)
doc.add_paragraph()
add_hr()
add_centered("PROJECT REPORT", 22, True, SRM_BLUE)
add_centered("Project Review — II", 14, False, GRAY)
add_hr()
doc.add_paragraph()
add_centered("MindSync AI", 36, True, SRM_BLUE)
add_centered("AI-Powered Healthcare Intelligence Platform", 16, False, GRAY)
doc.add_paragraph()
add_centered("Mental Health Support  •  Clinical Reports  •  Symptom Assessment  •  Mood Tracking", 11, False, GRAY)
doc.add_paragraph()
doc.add_paragraph()
doc.add_paragraph()

# Team info
t = doc.add_table(rows=2, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.cell(0, 0).text = "Submitted by:"
t.cell(1, 0).text = "Aditya Singh\nReg. No.: RAXXXXXXXXX\nB.Tech CSE"
t.cell(0, 1).text = "Under the Guidance of:"
t.cell(1, 1).text = "Dr. [Faculty Name]\nDept. of CSE\nSRMIST"
for row in t.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(11)
                run.font.name = 'Calibri'
        cell.paragraphs[0].runs[0].font.bold = True if cell.paragraphs[0].text.startswith(("Submitted", "Under")) else False

doc.add_paragraph()
add_centered("Academic Year 2025–2026", 13, True, GRAY)

page_break()

# =====================================================
# CERTIFICATE
# =====================================================

add_centered("CERTIFICATE", 22, True, SRM_BLUE, 20)
doc.add_paragraph()

add_para(
    'This is to certify that the project titled "MindSync AI — AI-Powered Healthcare Intelligence Platform" '
    'submitted by Aditya Singh (Reg. No.: RAXXXXXXXXX) in partial fulfillment of the requirements for the '
    'award of the degree of Bachelor of Technology in Computer Science and Engineering at SRM Institute of '
    'Science and Technology, Kattankulathur is a bonafide record of work carried out under my supervision '
    'during the academic year 2025–2026.', 12, False, DARK, 12)

doc.add_paragraph()
doc.add_paragraph()
doc.add_paragraph()

t = doc.add_table(rows=1, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.cell(0, 0).text = "____________________\nDr. [Faculty Name]\nProject Guide\nDept. of CSE, SRMIST"
t.cell(0, 1).text = "____________________\nHead of Department\nDept. of CSE\nSRMIST"

doc.add_paragraph()
add_para("Date: __________                    Place: Kattankulathur", 11, False, GRAY)

page_break()

# =====================================================
# ACKNOWLEDGEMENT
# =====================================================

add_centered("ACKNOWLEDGEMENT", 22, True, SRM_BLUE, 20)
doc.add_paragraph()

add_para(
    'I would like to express my sincere gratitude to my project guide Dr. [Faculty Name], Department of '
    'Computer Science and Engineering, SRM Institute of Science and Technology, for the invaluable guidance, '
    'constant encouragement, and support throughout the development of this project.', 12)

add_para(
    'I am thankful to the Head of the Department and all the faculty members of the Department of Computer '
    'Science and Engineering for providing the necessary resources and a conducive environment for this project work.', 12)

add_para(
    'I also extend my appreciation to the open-source community behind Ollama, Flask, and the Qwen language model, '
    'whose tools made this project possible.', 12)

add_para('Finally, I am grateful to my family and friends for their constant support and motivation.', 12)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run = p.add_run("Aditya Singh\nReg. No.: RAXXXXXXXXX")
run.font.bold = True
run.font.size = Pt(12)

page_break()

# =====================================================
# ABSTRACT
# =====================================================

add_centered("ABSTRACT", 22, True, SRM_BLUE, 20)
doc.add_paragraph()

add_para(
    'Mental health disorders affect a significant portion of the global population, yet access to qualified '
    'mental health professionals remains limited. Existing AI-based mental health tools often rely on cloud-based '
    'processing, raising serious concerns about patient data privacy and confidentiality.', 12, space_after=10)

add_para(
    'MindSync AI is an AI-powered healthcare intelligence platform designed to provide secure, offline clinical '
    'consultations using locally-hosted large language models. Built with Flask (Python) as the backend and vanilla '
    'HTML/CSS/JavaScript for the frontend, the platform runs the Qwen 2.5 (3B parameter) model through Ollama, '
    'ensuring that all patient data remains on the user\'s device with zero cloud dependency.', 12, space_after=10)

add_para(
    'The platform offers five core modules: (1) Patient Management with full CRUD operations, (2) AI-Powered Clinical '
    'Consultation with context-aware conversations and crisis detection, (3) Automated Clinical Report Generation with '
    'AI-driven risk assessment, (4) Symptom Assessment and Triage with urgency classification, and (5) Mood Tracking '
    'with historical visualization.', 12, space_after=10)

add_para(
    'Key safety features include a crisis keyword detection filter that provides immediate helpline contacts, message '
    'length validation, input sanitization against XSS attacks, and clear disclaimers encouraging professional medical '
    'consultation.', 12, space_after=10)

add_para(
    'Keywords: Artificial Intelligence, Mental Health, Healthcare Chatbot, NLP, Ollama, Qwen, Flask, '
    'Offline AI, Clinical Report Generation, Mood Tracking', 11, True, GRAY, 10)

page_break()

# =====================================================
# TABLE OF CONTENTS
# =====================================================

add_centered("TABLE OF CONTENTS", 22, True, SRM_BLUE, 20)
doc.add_paragraph()

toc_items = [
    ("1.", "Introduction", "1"),
    ("  1.1", "Overview", "1"),
    ("  1.2", "Problem Statement", "2"),
    ("  1.3", "Objectives", "2"),
    ("  1.4", "Scope", "3"),
    ("2.", "Literature Survey", "4"),
    ("3.", "System Design", "6"),
    ("  3.1", "Proposed System", "6"),
    ("  3.2", "System Architecture", "6"),
    ("  3.3", "Data Model", "7"),
    ("4.", "Module Description", "8"),
    ("  4.1", "Patient Management", "8"),
    ("  4.2", "Session Management", "8"),
    ("  4.3", "AI Chat Engine", "9"),
    ("  4.4", "Clinical Report Generator", "10"),
    ("  4.5", "Symptom Assessment & Triage", "11"),
    ("  4.6", "Mood Tracker", "11"),
    ("5.", "Implementation", "12"),
    ("  5.1", "Technology Stack", "12"),
    ("  5.2", "Backend Implementation", "12"),
    ("  5.3", "Frontend Implementation", "14"),
    ("  5.4", "AI Prompt Engineering", "15"),
    ("6.", "Testing and Results", "16"),
    ("7.", "Screenshots", "18"),
    ("8.", "Future Scope", "19"),
    ("9.", "Conclusion", "20"),
    ("", "References", "21"),
    ("", "Appendix A: File Structure", "22"),
    ("", "Appendix B: Installation Guide", "22"),
]

for num, title, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    if num.startswith("  "):
        run = p.add_run(f"     {num}  {title}")
        run.font.size = Pt(11)
    else:
        run = p.add_run(f"{num}  {title}")
        run.font.size = Pt(12)
        run.font.bold = True
    run.font.name = 'Calibri'

page_break()

# =====================================================
# CHAPTER 1: INTRODUCTION
# =====================================================

doc.add_heading('1. Introduction', level=1)

doc.add_heading('1.1 Overview', level=2)

add_para(
    'Mental health is one of the most pressing healthcare challenges of the 21st century. According to the '
    'World Health Organization (WHO), approximately 1 in every 8 people globally lives with a mental health '
    'condition, and the gap between those who need treatment and those who receive it remains alarmingly wide. '
    'In low- and middle-income countries, more than 75% of people with mental health conditions receive no treatment at all.', 12, space_after=10)

add_para(
    'The advent of Artificial Intelligence (AI) and Natural Language Processing (NLP) has opened new avenues '
    'for mental health support. AI-powered chatbots and virtual assistants can provide preliminary guidance, '
    'emotional support, and structured clinical tools to bridge the gap between patients and healthcare professionals. '
    'However, most existing solutions are cloud-based, requiring patient data to be transmitted to remote servers '
    '— a significant concern for sensitive medical information.', 12, space_after=10)

add_para(
    'MindSync AI addresses these limitations by providing a fully offline, locally-hosted AI healthcare platform. '
    'By leveraging the Ollama runtime with the Qwen 2.5 (3B) language model, all AI inference occurs on the '
    'user\'s machine, ensuring complete data privacy while maintaining clinical accuracy.', 12, space_after=10)

doc.add_heading('1.2 Problem Statement', level=2)

problems = [
    "Limited Access to Mental Health Professionals: The global shortage of mental health practitioners means many patients cannot receive timely care.",
    "Privacy Concerns: Existing AI mental health tools (e.g., Woebot, Wysa) transmit sensitive patient conversations to cloud servers, violating patient privacy expectations.",
    "Administrative Burden: Therapists and clinicians spend significant time on documentation — writing session notes, progress reports, and tracking patient mood patterns.",
    "Lack of Unified Platforms: No single platform combines AI consultation, clinical report generation, symptom triage, and mood tracking in an offline package.",
    "Stigma Barrier: Many individuals hesitate to seek help due to social stigma; a private AI assistant can serve as an initial bridge to professional care.",
]
for p in problems:
    add_numbered(p)

doc.add_heading('1.3 Objectives', level=2)

objectives = [
    "Develop an AI-powered healthcare assistant capable of conducting empathetic, clinically informed conversations.",
    "Implement a structured patient and session management system with full CRUD operations.",
    "Enable automated clinical report generation using AI analysis of patient conversation history.",
    "Provide a quick symptom assessment feature with urgency level classification and specialist recommendations.",
    "Build a mood tracking system to log and visualize patient emotional patterns over time.",
    "Ensure 100% offline operation with all AI inference running locally — no cloud dependency.",
    "Design a modern, responsive web interface accessible from any device on the local network.",
]
for o in objectives:
    add_numbered(o)

doc.add_heading('1.4 Scope', level=2)

scopes = [
    "Mental health professionals who need AI-assisted documentation for patient interactions.",
    "Clinics and hospitals seeking offline-capable AI consultation tools that preserve data privacy.",
    "Researchers studying mood patterns and therapy outcomes through data-driven insights.",
    "Patients seeking initial guidance on symptoms before consulting a specialist.",
]
for s in scopes:
    add_bullet(s)

page_break()

# =====================================================
# CHAPTER 2: LITERATURE SURVEY
# =====================================================

doc.add_heading('2. Literature Survey', level=1)

add_para(
    'A comprehensive review of existing literature and tools was conducted to identify the current state '
    'of AI-assisted mental health care and the gaps that MindSync AI aims to address.', 12, space_after=10)

doc.add_heading('2.1 Woebot (Fitzpatrick et al., 2017)', level=2)
add_para(
    'Woebot is a conversational agent designed to deliver Cognitive Behavioral Therapy (CBT) techniques to '
    'young adults. In a randomized controlled trial, participants who used Woebot for two weeks showed significant '
    'reduction in depression symptoms compared to the control group.', 12, space_after=6)
add_para('Limitations: Rule-based conversational patterns; no clinical reporting or patient management.', 11, False, GRAY, 10)

doc.add_heading('2.2 Wysa (Inkster et al., 2018)', level=2)
add_para(
    'Wysa is an AI-powered mental health chatbot combining NLP with therapeutic techniques (CBT, DBT, mindfulness). '
    'Studies showed significant improvement in PHQ-9 depression scores among users.', 12, space_after=6)
add_para('Limitations: Cloud-based (privacy concern); no report generation feature.', 11, False, GRAY, 10)

doc.add_heading('2.3 Large Language Models in Healthcare (Singhal et al., 2023)', level=2)
add_para(
    'Google\'s Med-PaLM demonstrated that LLMs can achieve expert-level accuracy on medical QA benchmarks (USMLE). '
    'This validated the potential of LLMs for clinical applications.', 12, space_after=6)
add_para('Limitations: Requires cloud GPUs; not designed for therapy/counseling use cases.', 11, False, GRAY, 10)

doc.add_heading('2.4 Ollama and Local LLMs (2024)', level=2)
add_para(
    'The Ollama project enables running large language models locally on consumer hardware without cloud infrastructure.', 12, space_after=6)
add_para('Gap: No healthcare-specific application framework exists that leverages local LLMs.', 11, False, GRAY, 10)

doc.add_heading('2.5 Comparison Table', level=2)

add_table(
    ["Feature", "Woebot", "Wysa", "Med-PaLM", "MindSync AI"],
    [
        ["AI Conversations", "Yes", "Yes", "Yes", "Yes"],
        ["Offline / Local AI", "No", "No", "No", "Yes"],
        ["Clinical Reports", "No", "No", "No", "Yes"],
        ["Symptom Triage", "No", "Partial", "Yes", "Yes"],
        ["Mood Tracking", "No", "Yes", "No", "Yes"],
        ["Patient Management", "No", "No", "No", "Yes"],
        ["Data Privacy", "Cloud", "Cloud", "Cloud", "Local"],
    ]
)

page_break()

# =====================================================
# CHAPTER 3: SYSTEM DESIGN
# =====================================================

doc.add_heading('3. System Design', level=1)

doc.add_heading('3.1 Proposed System', level=2)
add_para(
    'MindSync AI is a web-based healthcare intelligence platform built on a three-tier architecture:', 12, space_after=6)
add_numbered('Presentation Layer: HTML5/CSS3/JavaScript frontend served by Flask\'s template engine.')
add_numbered('Application Layer: Flask (Python) REST API handling all business logic and routing.')
add_numbered('AI + Data Layer: Ollama runtime with Qwen 2.5:3B model and JSON file-based storage.')

doc.add_heading('3.2 System Architecture', level=2)

add_para('The system follows a layered architecture pattern:', 12, space_after=10)

arch_layers = [
    ("PRESENTATION LAYER", "HTML5 / CSS3 / JavaScript (Vanilla ES6+)", "index.html  |  styles.css  |  app.js"),
    ("", "↓ HTTP / REST API ↓", ""),
    ("APPLICATION LAYER", "Flask (Python 3.12) — 14 API Routes", "Patient CRUD | Chat | Reports | Assessment | Mood"),
    ("", "↓ Ollama SDK ↓", ""),
    ("AI ENGINE", "Ollama + Qwen 2.5:3B (Local LLM)", "System Prompts | Safety Filters | Context Windowing"),
    ("", "↓ File I/O ↓", ""),
    ("DATA LAYER", "JSON File Storage (chat.json)", "Patients | Sessions | Messages | Mood Logs"),
]

for layer, tech, detail in arch_layers:
    if layer:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(f"  [{layer}]")
        run.font.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Consolas'
        run2 = p.add_run(f"\n    {tech}")
        run2.font.size = Pt(10)
        run2.font.name = 'Consolas'
        if detail:
            run3 = p.add_run(f"\n    {detail}")
            run3.font.size = Pt(10)
            run3.font.name = 'Consolas'
            run3.font.color.rgb = GRAY
    else:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(tech)
        run.font.size = Pt(10)
        run.font.name = 'Consolas'
        run.font.color.rgb = GRAY

doc.add_heading('3.3 Data Model', level=2)

add_para('The application uses a JSON-based data structure for patient records:', 12, space_after=6)

data_model = """Patient Record:
{
    "id": "UUID string",
    "name": "Patient Name",
    "age": "Age (optional)",
    "gender": "Gender (optional)",
    "sessions": [
        {
            "id": "UUID string",
            "name": "Session Name",
            "created_at": "DD/MM/YYYY - HH:MM",
            "messages": [
                {"type": "user", "text": "..."},
                {"type": "bot",  "text": "..."}
            ]
        }
    ],
    "mood_logs": [
        {
            "score": "1-10",
            "note": "Optional text",
            "timestamp": "DD/MM/YYYY - HH:MM"
        }
    ]
}"""

p = doc.add_paragraph()
run = p.add_run(data_model)
run.font.name = 'Consolas'
run.font.size = Pt(10)

page_break()

# =====================================================
# CHAPTER 4: MODULE DESCRIPTION
# =====================================================

doc.add_heading('4. Module Description', level=1)

# Module 1
doc.add_heading('4.1 Patient Management', level=2)
add_para('This module handles the complete lifecycle of patient records.', 12, space_after=6)
add_para('Features:', 12, True, space_after=4)
add_bullet('Create new patients with name, age, and gender fields')
add_bullet('Rename and delete existing patients')
add_bullet('Each patient is assigned a unique UUID for identification')
add_bullet('Search and filter across all patients, sessions, and message content')
add_para('API Endpoints:', 12, True, space_after=4)
add_bullet('GET /get_patients — Retrieve all patient records')
add_bullet('POST /add_patient — Create a new patient')
add_bullet('POST /rename_patient — Rename an existing patient')
add_bullet('POST /delete_patient — Delete a patient and all associated data')
add_bullet('POST /export_patient — Export complete patient data as JSON')

# Module 2
doc.add_heading('4.2 Session Management', level=2)
add_para('Each patient can have multiple chat sessions, organized by visit, topic, or date.', 12, space_after=6)
add_para('Features:', 12, True, space_after=4)
add_bullet('Create new sessions under any patient')
add_bullet('Rename and delete sessions independently')
add_bullet('Each session stores its own message history with timestamps')
add_bullet('Sessions displayed in hover-dropdown under each patient name')
add_para('API Endpoints:', 12, True, space_after=4)
add_bullet('POST /add_session — Create a new session')
add_bullet('POST /rename_session — Rename a session')
add_bullet('POST /delete_session — Delete a session')

# Module 3
doc.add_heading('4.3 AI Chat Engine', level=2)
add_para('The core module enabling real-time AI-powered clinical conversations.', 12, space_after=6)
add_para('Features:', 12, True, space_after=4)
add_bullet('Context-aware responses using the last 10 messages from the current session')
add_bullet('Clinically-focused system prompt for empathetic, evidence-based responses')
add_bullet('Safety filter detecting crisis keywords (suicide, kill myself, self harm, etc.)')
add_bullet('Automatic helpline display: iCall 9152987821, Vandrevala Foundation 1860-2662-345')
add_bullet('Message length validation (5000 character maximum)')
add_bullet('Voice input via Web Speech API and text-to-speech via SpeechSynthesis API')
add_para('API Endpoint: POST /chat', 12, True, space_after=4)

# Module 4
doc.add_heading('4.4 Clinical Report Generator', level=2)
add_para('Automated generation of structured clinical reports using AI analysis.', 12, space_after=6)
add_para('Report Sections:', 12, True, space_after=4)
add_numbered('Patient Summary — Overview of presenting complaints and conditions')
add_numbered('Medical Conditions Identified — Symptoms, medications, lab values')
add_numbered('Mental Health Assessment — Emotional state, anxiety/depression indicators')
add_numbered('Risk Level — LOW / MODERATE / HIGH with justification')
add_numbered('Progress & Trends — Improvements or regressions across sessions')
add_numbered('Clinical Recommendations — Next steps, referrals, lifestyle changes')
add_para('Additional Features:', 12, True, space_after=4)
add_bullet('Stats cards: total sessions, messages, average messages per session')
add_bullet('Session-by-session breakdown grid')
add_bullet('Formatted AI analysis with headings, bold text, and bullet points')
add_bullet('Print-friendly report output (opens in new browser window)')
add_para('API Endpoint: POST /generate_report', 12, True, space_after=4)

# Module 5
doc.add_heading('4.5 Symptom Assessment & Triage', level=2)
add_para('Quick AI-powered tool for preliminary symptom evaluation.', 12, space_after=6)
add_para('Output Format:', 12, True, space_after=4)
add_numbered('Possible Conditions — 2-4 conditions (most likely first)')
add_numbered('Urgency Level — ROUTINE / SOON / URGENT / EMERGENCY')
add_numbered('Recommended Specialist — Type of doctor to consult')
add_numbered('Immediate Steps — What the patient should do now')
add_para('API Endpoint: POST /health_assessment', 12, True, space_after=4)

# Module 6
doc.add_heading('4.6 Mood Tracker', level=2)
add_para('Longitudinal tracking of patient mood patterns.', 12, space_after=6)
add_para('Features:', 12, True, space_after=4)
add_bullet('Mood score slider from 1 (Very Low) to 10 (Excellent)')
add_bullet('Optional text note for context')
add_bullet('Per-patient mood logging with automatic timestamps')
add_bullet('Color-coded mood history: Red (1-3), Yellow (4-6), Green (7-10)')
add_para('API Endpoints:', 12, True, space_after=4)
add_bullet('POST /log_mood — Log a mood score for a patient')
add_bullet('POST /get_mood_logs — Retrieve mood history for a patient')

page_break()

# =====================================================
# CHAPTER 5: IMPLEMENTATION
# =====================================================

doc.add_heading('5. Implementation', level=1)

doc.add_heading('5.1 Technology Stack', level=2)

add_table(
    ["Component", "Technology"],
    [
        ["Programming Language", "Python 3.12"],
        ["Web Framework", "Flask 3.x"],
        ["AI Runtime", "Ollama (Local LLM Engine)"],
        ["AI Model", "Qwen 2.5:3B (3 billion parameters)"],
        ["Frontend Markup", "HTML5"],
        ["Styling", "CSS3 (Custom Properties, Grid, Flexbox, Animations)"],
        ["Frontend Logic", "JavaScript ES6+ (Vanilla, no framework)"],
        ["Voice Features", "Web Speech API (SpeechRecognition + SpeechSynthesis)"],
        ["Data Storage", "JSON file (chat.json)"],
        ["ID Generation", "Python UUID module"],
        ["Font", "Inter (Google Fonts CDN)"],
        ["IDE", "Visual Studio Code"],
    ]
)

doc.add_heading('5.2 Backend Implementation', level=2)

add_para('The backend is a single Flask application (app.py) with 14 RESTful API endpoints.', 12, space_after=6)
add_para('Key Backend Components:', 12, True, space_after=4)
add_bullet('File Helpers: load_data(), save_data(), find_patient(), find_session() — manage JSON I/O with error recovery')
add_bullet('Safety Filter: is_sensitive() checks messages against crisis keywords')
add_bullet('AI Integration: get_qwen_response() calls Ollama with temperature 0.7, top-p 0.9')
add_bullet('Context Windowing: Last 10 messages per session sent to AI')

doc.add_heading('API Routes Summary', level=3)

add_table(
    ["Route", "Method", "Description"],
    [
        ["/", "GET", "Serve landing page"],
        ["/get_patients", "GET", "Retrieve all patients"],
        ["/add_patient", "POST", "Create new patient"],
        ["/rename_patient", "POST", "Rename patient"],
        ["/delete_patient", "POST", "Delete patient"],
        ["/add_session", "POST", "Create session under patient"],
        ["/rename_session", "POST", "Rename session"],
        ["/delete_session", "POST", "Delete session"],
        ["/chat", "POST", "Send message, receive AI response"],
        ["/generate_report", "POST", "Generate clinical report"],
        ["/log_mood", "POST", "Log mood score"],
        ["/get_mood_logs", "POST", "Get mood history"],
        ["/health_assessment", "POST", "Symptom triage"],
        ["/export_patient", "POST", "Export patient data"],
    ]
)

doc.add_heading('5.3 Frontend Implementation', level=2)

add_para('User Interface Design:', 12, True, space_after=4)
add_bullet('Dark theme with CSS custom properties (design tokens)')
add_bullet('Background: #060d18 (deep navy), Primary: #4e9fff (blue), Accent: #34d399 (green)')
add_bullet('Inter font family via Google Fonts CDN')
add_bullet('Responsive design with breakpoints at 1024px, 768px, and 480px')

add_para('UI Patterns:', 12, True, space_after=4)
add_numbered('Loading Screen — Animated dual-ring spinner with progress bar and 5-step text sequence')
add_numbered('Hero Section — Dashboard with live counters and call-to-action buttons')
add_numbered('Feature Cards — Four cards with SVG icons for each core feature')
add_numbered('Full-Screen Overlays — Used for Chat and Report interfaces with sidebar navigation')
add_numbered('Modal Dialogs — Used for Symptom Assessment and Mood Tracker')

add_para('JavaScript Architecture:', 12, True, space_after=4)
add_bullet('apiGet() / apiPost() — Centralized HTTP request handlers with error handling')
add_bullet('escapeHtml() — XSS prevention for all dynamic content')
add_bullet('renderPatients() — Dynamic sidebar with hover dropdowns and context menus')
add_bullet('formatAnalysis() — Markdown-to-HTML converter for AI output')
add_bullet('animateCounter() — Smooth counting animation for dashboard stats')
add_bullet('speak() — Text-to-speech wrapper using SpeechSynthesis API')

doc.add_heading('5.4 AI Prompt Engineering', level=2)

add_para('Three distinct system prompts are engineered for different AI tasks:', 12, space_after=6)
add_numbered('Chat Prompt: Empathetic, clinically accurate, reference medications/lab values, never diagnose')
add_numbered('Report Prompt: 6-section structured clinical report with risk level classification')
add_numbered('Triage Prompt: Possible conditions, urgency level, specialist, immediate steps')

page_break()

# =====================================================
# CHAPTER 6: TESTING
# =====================================================

doc.add_heading('6. Testing and Results', level=1)

doc.add_heading('6.1 Functional Testing', level=2)

add_table(
    ["#", "Test Case", "Expected Result", "Status"],
    [
        ["1", "Create a new patient", "Patient appears in sidebar with UUID", "Pass"],
        ["2", "Rename a patient", "Name updates across all views", "Pass"],
        ["3", "Delete a patient", "Patient removed from list and JSON", "Pass"],
        ["4", "Create a session", "Session appears in patient dropdown", "Pass"],
        ["5", "Send chat message", "AI responds contextually", "Pass"],
        ["6", "Trigger crisis keyword", "Safety message with helplines shown", "Pass"],
        ["7", "Generate report", "Structured report with AI analysis", "Pass"],
        ["8", "Submit symptom assessment", "Triage output with urgency level", "Pass"],
        ["9", "Log mood score", "Mood entry saved and displayed", "Pass"],
        ["10", "Search patients", "Filters across names/sessions/messages", "Pass"],
    ]
)

doc.add_heading('6.2 Edge Case Testing', level=2)

add_table(
    ["#", "Scenario", "Expected Behavior", "Status"],
    [
        ["1", "Report for patient with no sessions", "Error message displayed", "Pass"],
        ["2", "Message exceeding 5000 chars", "Rejected with error", "Pass"],
        ["3", "Corrupted chat.json", "Auto-recovery with empty array", "Pass"],
        ["4", "Empty patient name", "Auto-assigned 'Patient N'", "Pass"],
        ["5", "Mood score outside 1-10", "Server validation rejects", "Pass"],
    ]
)

doc.add_heading('6.3 UI/UX Testing', level=2)
add_bullet('Responsive layout verified at 1024px, 768px, and 480px breakpoints')
add_bullet('Loading screen animation and progress bar render correctly')
add_bullet('Report loading spinner hides properly after generation (CSS !important fix)')
add_bullet('Modal open/close behavior verified for Assessment and Mood')
add_bullet('Voice input and TTS functional in Chrome and Edge')

doc.add_heading('6.4 Performance', level=2)
add_bullet('Flask server startup: < 2 seconds')
add_bullet('AI response latency: 3–8 seconds (hardware dependent)')
add_bullet('Report generation: 5–15 seconds (includes AI analysis)')
add_bullet('Frontend renders 50+ messages smoothly')
add_bullet('JSON handles 100+ patients without lag')

page_break()

# =====================================================
# CHAPTER 7: SCREENSHOTS
# =====================================================

doc.add_heading('7. Screenshots', level=1)

add_para(
    'Note: Insert screenshots of the application here. Recommended screenshots:', 12, False, GRAY, 10)

screenshots = [
    "Landing page / Dashboard with hero section and feature cards",
    "Loading screen with animated spinner and progress bar",
    "Chat overlay with patient sidebar and AI conversation",
    "Clinical report view with stats cards and AI analysis",
    "Symptom assessment modal with triage output",
    "Mood tracker modal with slider and history display",
    "Crisis keyword detection showing helpline numbers",
    "Print-friendly report output",
]
for s in screenshots:
    add_numbered(s)

add_para('\n[Insert screenshots here]\n', 14, True, GRAY, 10)

page_break()

# =====================================================
# CHAPTER 8: FUTURE SCOPE
# =====================================================

doc.add_heading('8. Future Scope', level=1)

future_items = [
    ("Interactive Mood Charts", "Replace text-based mood history with interactive line and bar charts using Chart.js for visual trend analysis."),
    ("Database Migration", "Migrate from JSON file storage to SQLite or PostgreSQL for improved scalability and concurrency."),
    ("User Authentication", "Implement login system with role-based access (doctor vs. patient vs. admin)."),
    ("PDF Report Export", "Generate downloadable PDF clinical reports with custom hospital branding."),
    ("Larger AI Models", "Support for Llama 3, Mistral, or GPT-4 to improve response accuracy."),
    ("Multi-Language Support", "Add Hindi, Tamil, and other regional Indian languages for wider reach."),
    ("Progressive Web App", "Convert to PWA for mobile access with offline caching."),
    ("Continuous Voice Mode", "Implement continuous speech recognition for hands-free documentation."),
    ("Appointment Scheduling", "Add module for follow-up appointment scheduling with reminders."),
    ("EHR Integration", "Support HL7 FHIR standards for Electronic Health Record interoperability."),
]

for title, desc in future_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(f"{title}: ")
    run.font.bold = True
    run.font.size = Pt(12)
    run2 = p.add_run(desc)
    run2.font.size = Pt(12)

page_break()

# =====================================================
# CHAPTER 9: CONCLUSION
# =====================================================

doc.add_heading('9. Conclusion', level=1)

add_para(
    'MindSync AI successfully demonstrates that a fully offline, AI-powered healthcare intelligence platform '
    'is both feasible and practical using current open-source technologies. The project achieves all stated objectives:', 12, space_after=10)

conclusions = [
    "AI-Powered Consultations: The Qwen 2.5 model delivers contextually relevant, empathetic clinical conversations.",
    "Patient Management: Full CRUD operations with UUID-based identification and search functionality.",
    "Clinical Reports: Automated AI-generated reports with risk level classification and actionable recommendations.",
    "Symptom Triage: Quick AI-powered assessment with urgency levels from ROUTINE to EMERGENCY.",
    "Mood Tracking: Per-patient mood logging with color-coded visualization and historical review.",
    "Complete Privacy: Zero cloud dependency — all AI inference and data storage occurs locally.",
    "Modern UI: Responsive dark-themed design accessible from any device on the local network.",
]
for c in conclusions:
    add_numbered(c)

doc.add_paragraph()
add_para(
    'The safety-first approach — with crisis detection, helpline contacts, input validation, XSS prevention, '
    'and clear medical disclaimers — ensures the system supports rather than replaces professional healthcare providers.', 12, space_after=10)

add_para(
    'While limitations exist (3B model accuracy, JSON scalability, no authentication), the platform provides a '
    'strong foundation for future development into a production-grade healthcare tool.', 12, space_after=10)

page_break()

# =====================================================
# REFERENCES
# =====================================================

doc.add_heading('References', level=1)

refs = [
    '[1] Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). "Delivering Cognitive Behavior Therapy to Young Adults via a Fully Automated Conversational Agent (Woebot)." JMIR Mental Health, 4(2), e19.',
    '[2] Inkster, B., Sarda, S., & Subramanian, V. (2018). "An Empathy-Driven, Conversational AI Agent (Wysa) for Digital Mental Well-Being." JMIR mHealth and uHealth, 6(11), e12106.',
    '[3] Singhal, K., et al. (2023). "Large Language Models Encode Clinical Knowledge." Nature, 620, 172–180.',
    '[4] Ollama Documentation — https://ollama.com/docs',
    '[5] Qwen 2.5 Model Card — https://huggingface.co/Qwen/Qwen2.5-3B',
    '[6] Flask Documentation — https://flask.palletsprojects.com/',
    '[7] Web Speech API — MDN Web Docs — https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API',
    '[8] WHO (2022). "World Mental Health Report: Transforming Mental Health for All." https://www.who.int/publications/i/item/9789240049338',
]

for r in refs:
    add_para(r, 11, space_after=8)

page_break()

# =====================================================
# APPENDIX
# =====================================================

doc.add_heading('Appendix A: Project File Structure', level=1)

file_struct = """MindSync AI/
├── app.py                  # Flask backend (14 API routes)
├── chat.json               # Patient data storage
├── requirement.txt         # Python dependencies
├── generate_ppt.py         # PPT generation script
├── templates/
│   └── index.html          # Main HTML page
└── static/
    ├── css/
    │   └── styles.css      # Application stylesheet
    └── js/
        └── app.js          # Frontend JavaScript"""

p = doc.add_paragraph()
run = p.add_run(file_struct)
run.font.name = 'Consolas'
run.font.size = Pt(11)

doc.add_paragraph()

doc.add_heading('Appendix B: Installation Guide', level=1)

install_steps = [
    "Install Python 3.12+ from https://python.org",
    "Install Ollama from https://ollama.com",
    "Pull the AI model: ollama pull qwen2.5:3b",
    "Install Python dependencies: pip install flask ollama",
    "Run the application: python app.py",
    "Open in browser: http://localhost:5000",
]
for s in install_steps:
    add_numbered(s)


# =====================================================
# SAVE
# =====================================================

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MindSync_AI_Project_Report.docx")
doc.save(output_path)
print(f"\nReport saved to: {output_path}")
