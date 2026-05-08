from flask import Flask, render_template, request, jsonify
import ollama
import os
import json
import logging
import uuid
from datetime import datetime

app = Flask(__name__)

CHAT_FILE = "chat.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------- FILE HELPERS ----------------

def ensure_chat_file():
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def load_data():
    ensure_chat_file()
    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []


def save_data(data):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def find_patient(data, patient_id):
    for patient in data:
        if patient["id"] == patient_id:
            return patient
    return None


def find_session(patient, session_id):
    for session in patient.get("sessions", []):
        if session["id"] == session_id:
            return session
    return None


# ---------------- SAFETY FILTER ----------------

def is_sensitive(text):
    keywords = ["suicide", "kill myself", "end my life", "die", "self harm", "cut myself"]
    return any(k in text.lower() for k in keywords)


# ---------------- AI ----------------

def get_qwen_response(messages):
    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=messages,
            options={
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        return response["message"]["content"]

    except Exception as e:
        logger.error(f"Ollama Error: {str(e)}")
        return "I'm having trouble processing your request right now. Please try again."


# ---------------- PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PATIENT ROUTES ----------------

@app.route("/get_patients", methods=["GET"])
def get_patients():
    data = load_data()
    return jsonify(data)


@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_name = payload.get("name", "").strip()
    if not patient_name:
        patient_name = f"Patient {len(data) + 1}"

    new_patient = {
        "id": str(uuid.uuid4()),
        "name": patient_name,
        "age": payload.get("age", ""),
        "gender": payload.get("gender", ""),
        "sessions": []
    }

    data.append(new_patient)
    save_data(data)

    return jsonify(new_patient), 201


@app.route("/rename_patient", methods=["POST"])
def rename_patient():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    new_name = payload.get("name", "").strip()

    if not patient_id or not new_name:
        return jsonify({"error": "patient_id and name are required"}), 400

    patient = find_patient(data, patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient["name"] = new_name
    save_data(data)

    return jsonify({"status": "ok"})


@app.route("/delete_patient", methods=["POST"])
def delete_patient():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    updated = [p for p in data if p["id"] != patient_id]

    if len(updated) == len(data):
        return jsonify({"error": "Patient not found"}), 404

    save_data(updated)
    return jsonify({"status": "ok"})


# ---------------- SESSION ROUTES ----------------

@app.route("/add_session", methods=["POST"])
def add_session():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    session_name = payload.get("name", "").strip()

    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    patient = find_patient(data, patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    if not session_name:
        session_name = f"Session {len(patient['sessions']) + 1}"

    new_session = {
        "id": str(uuid.uuid4()),
        "name": session_name,
        "created_at": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "messages": []
    }

    patient["sessions"].append(new_session)
    save_data(data)

    return jsonify(new_session), 201


@app.route("/rename_session", methods=["POST"])
def rename_session():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    session_id = payload.get("session_id", "").strip()
    new_name = payload.get("name", "").strip()

    if not patient_id or not session_id or not new_name:
        return jsonify({"error": "patient_id, session_id and name are required"}), 400

    patient = find_patient(data, patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    session = find_session(patient, session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    session["name"] = new_name
    save_data(data)

    return jsonify({"status": "ok"})


@app.route("/delete_session", methods=["POST"])
def delete_session():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    session_id = payload.get("session_id", "").strip()

    if not patient_id or not session_id:
        return jsonify({"error": "patient_id and session_id are required"}), 400

    patient = find_patient(data, patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    original_len = len(patient["sessions"])
    patient["sessions"] = [s for s in patient["sessions"] if s["id"] != session_id]

    if len(patient["sessions"]) == original_len:
        return jsonify({"error": "Session not found"}), 404

    save_data(data)
    return jsonify({"status": "ok"})


# ---------------- CHAT ROUTE ----------------

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = load_data()
        payload = request.get_json(silent=True) or {}

        patient_id = payload.get("patient_id", "").strip()
        session_id = payload.get("session_id", "").strip()
        user_message = payload.get("message", "").strip()

        if not patient_id or not session_id:
            return jsonify({"response": "patient_id and session_id are required"}), 400

        if not user_message:
            return jsonify({"response": "Please provide a valid message"}), 400

        if len(user_message) > 5000:
            return jsonify({"response": "Message too long"}), 400

        if is_sensitive(user_message):
            return jsonify({
                "response": (
                    "I'm really sorry you're feeling this way. You're not alone. "
                    "Please consider talking to someone you trust or a professional. "
                    "If you're in immediate danger, please contact local help services. "
                    "National helpline: iCall 9152987821 | Vandrevala Foundation 1860-2662-345"
                )
            })

        patient = find_patient(data, patient_id)
        if not patient:
            return jsonify({"response": "Patient not found"}), 404

        session = find_session(patient, session_id)
        if not session:
            return jsonify({"response": "Session not found"}), 404

        session["messages"].append({
            "type": "user",
            "text": user_message
        })

        messages = [
            {
                "role": "system",
                "content": (
                    "You are MindSync AI, a strictly healthcare and mental health assistant. "
                    "You ONLY discuss topics related to physical health, mental health, medical conditions, symptoms, medications, therapy, and wellness. "
                    "If the user asks about anything unrelated to health or mental wellness (such as finance, technology, entertainment, vehicles, or any non-health topic), "
                    "you must politely decline and redirect them by saying: 'I'm a healthcare assistant and can only help with health and mental wellness topics. Is there something health-related I can help you with?'\n"
                    "- Be empathetic, calm, and clinically accurate\n"
                    "- Provide evidence-based medical and psychological guidance\n"
                    "- Reference relevant medical conditions, medications, and treatments when appropriate\n"
                    "- Use structured responses with clear sections when giving detailed advice\n"
                    "- Do not diagnose — suggest the patient discuss with their doctor\n"
                    "- Encourage healthy coping strategies and lifestyle modifications\n"
                    "- If the patient mentions specific lab values or medications, address them knowledgeably\n"
                    "- Always prioritize patient safety\n"
                )
            }
        ]

        for msg in session["messages"][-10:]:
            role = "user" if msg["type"] == "user" else "assistant"
            messages.append({
                "role": role,
                "content": msg["text"]
            })

        ai_response = get_qwen_response(messages)

        session["messages"].append({
            "type": "bot",
            "text": ai_response
        })

        save_data(data)

        return jsonify({"response": ai_response})

    except Exception as e:
        logger.error(f"Chat Error: {str(e)}")
        return jsonify({"response": "An internal error occurred"}), 500


# ---------------- REPORT ROUTE ----------------

@app.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        data = load_data()
        payload = request.get_json(silent=True) or {}

        patient_id = payload.get("patient_id", "").strip()
        if not patient_id:
            return jsonify({"error": "patient_id is required"}), 400

        patient = find_patient(data, patient_id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        sessions = patient.get("sessions", [])
        if not sessions:
            return jsonify({"error": "No sessions found for this patient"}), 400

        total_messages = 0
        total_sessions = len(sessions)
        session_summaries = []

        for session in sessions:
            msgs = session.get("messages", [])
            total_messages += len(msgs)
            user_msgs = [m["text"] for m in msgs if m["type"] == "user"]
            bot_msgs = [m["text"] for m in msgs if m["type"] == "bot"]
            session_summaries.append({
                "name": session.get("name", "Unnamed"),
                "created_at": session.get("created_at", "N/A"),
                "message_count": len(msgs),
                "user_messages": user_msgs,
                "bot_messages": bot_msgs
            })

        all_user_messages = []
        for s in session_summaries:
            all_user_messages.extend(s["user_messages"])

        transcript = "\n".join(all_user_messages[-50:])

        analysis_prompt = [
            {
                "role": "system",
                "content": (
                    "You are a clinical healthcare analysis assistant. "
                    "Analyze the following patient messages from healthcare/therapy sessions and produce a structured medical report. "
                    "The report must include these sections:\n"
                    "1. **Patient Summary** — Brief overview of the patient's presenting complaints and conditions.\n"
                    "2. **Medical Conditions Identified** — List conditions, symptoms, medications, and lab values mentioned.\n"
                    "3. **Mental Health Assessment** — Evaluate emotional state, anxiety/depression indicators, coping capacity.\n"
                    "4. **Risk Level** — Assign LOW / MODERATE / HIGH risk with justification.\n"
                    "5. **Progress & Trends** — Note improvements, regressions, or patterns across sessions.\n"
                    "6. **Clinical Recommendations** — Suggest next steps, referrals, lifestyle changes, or treatment adjustments.\n\n"
                    "Be professional, evidence-based, and concise. Use bullet points. Do not fabricate data."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Patient Name: {patient['name']}\n"
                    f"Age: {patient.get('age', 'N/A')}\n"
                    f"Gender: {patient.get('gender', 'N/A')}\n"
                    f"Total Sessions: {total_sessions}\n"
                    f"Total Messages: {total_messages}\n\n"
                    f"Patient Messages:\n{transcript}"
                )
            }
        ]

        ai_analysis = get_qwen_response(analysis_prompt)

        report = {
            "patient_name": patient["name"],
            "patient_id": patient["id"],
            "patient_age": patient.get("age", "N/A"),
            "patient_gender": patient.get("gender", "N/A"),
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "sessions": [
                {
                    "name": s["name"],
                    "created_at": s["created_at"],
                    "message_count": s["message_count"]
                }
                for s in session_summaries
            ],
            "ai_analysis": ai_analysis,
            "generated_at": datetime.now().strftime("%d/%m/%Y - %H:%M")
        }

        return jsonify(report)

    except Exception as e:
        logger.error(f"Report Error: {str(e)}")
        return jsonify({"error": "Failed to generate report"}), 500


# ---------------- MOOD TRACKING ----------------

@app.route("/log_mood", methods=["POST"])
def log_mood():
    try:
        data = load_data()
        payload = request.get_json(silent=True) or {}

        patient_id = payload.get("patient_id", "").strip()
        mood_score = payload.get("mood_score")
        note = payload.get("note", "").strip()

        if not patient_id or mood_score is None:
            return jsonify({"error": "patient_id and mood_score are required"}), 400

        mood_score = int(mood_score)
        if mood_score < 1 or mood_score > 10:
            return jsonify({"error": "mood_score must be between 1 and 10"}), 400

        patient = find_patient(data, patient_id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        if "mood_logs" not in patient:
            patient["mood_logs"] = []

        patient["mood_logs"].append({
            "score": mood_score,
            "note": note,
            "timestamp": datetime.now().strftime("%d/%m/%Y - %H:%M")
        })

        save_data(data)

        return jsonify({"status": "ok"})

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid mood_score"}), 400


@app.route("/get_mood_logs", methods=["POST"])
def get_mood_logs():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    patient = find_patient(data, patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient.get("mood_logs", []))


# ---------------- QUICK HEALTH ASSESSMENT ----------------

@app.route("/health_assessment", methods=["POST"])
def health_assessment():
    try:
        payload = request.get_json(silent=True) or {}
        symptoms = payload.get("symptoms", "").strip()

        if not symptoms:
            return jsonify({"error": "Symptoms are required"}), 400

        if len(symptoms) > 5000:
            return jsonify({"error": "Input too long"}), 400

        messages = [
            {
                "role": "system",
                "content": (
                    "You are MindSync AI, a strictly healthcare triage assistant. "
                    "You ONLY assess health-related symptoms and medical concerns. "
                    "If the input is not related to health or medical symptoms, respond with: 'Please describe a health-related symptom or concern so I can assist you.' "
                    "Based on the symptoms described, provide:\n"
                    "1. **Possible Conditions** — List 2-4 possible conditions (most likely first)\n"
                    "2. **Urgency Level** — ROUTINE / SOON / URGENT / EMERGENCY\n"
                    "3. **Recommended Specialist** — Which type of doctor to see\n"
                    "4. **Immediate Steps** — What the patient should do now\n\n"
                    "DISCLAIMER: This is not a diagnosis. Always consult a healthcare professional.\n"
                    "Be professional, accurate, and reassuring."
                )
            },
            {
                "role": "user",
                "content": symptoms
            }
        ]

        response = get_qwen_response(messages)
        return jsonify({"assessment": response})

    except Exception as e:
        logger.error(f"Assessment Error: {str(e)}")
        return jsonify({"error": "Failed to generate assessment"}), 500


# ---------------- EXPORT PATIENT DATA ----------------

@app.route("/export_patient", methods=["POST"])
def export_patient():
    data = load_data()
    payload = request.get_json(silent=True) or {}

    patient_id = payload.get("patient_id", "").strip()
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    patient = find_patient(data, patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient)


# ---------------- RUN ----------------

if __name__ == "__main__":
    ensure_chat_file()
    app.run(host="0.0.0.0", port=5000, debug=True)