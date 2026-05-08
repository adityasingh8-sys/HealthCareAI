/* ==========================================
   MindSync AI — Frontend Application
   ========================================== */

// Cancel any leftover speech
if ("speechSynthesis" in window) speechSynthesis.cancel();

// ==========================================
// LOADING SCREEN
// ==========================================

document.documentElement.classList.add("loading");
document.body.classList.add("loading");

const loadingLines = [
  "INITIALIZING MINDSYNC...",
  "LOADING AI ENGINE...",
  "CONNECTING SERVICES...",
  "PREPARING DASHBOARD...",
  "READY"
];

let loadingStep = 0;
const loadingText = document.getElementById("loadingText");
const loadingBar = document.getElementById("loadingBar");

function advanceLoading() {
  if (!loadingText) return;
  loadingText.textContent = loadingLines[loadingStep];
  if (loadingBar) loadingBar.style.width = ((loadingStep + 1) / loadingLines.length * 100) + "%";
  loadingStep++;
  if (loadingStep < loadingLines.length) {
    setTimeout(advanceLoading, 900);
  } else {
    setTimeout(finishLoading, 700);
  }
}

function finishLoading() {
  const screen = document.getElementById("loading-screen");
  if (screen) screen.classList.add("hidden");
  document.documentElement.classList.remove("loading");
  document.body.classList.remove("loading");
  loadHeroStats();
}

advanceLoading();

// ==========================================
// DOM REFS
// ==========================================

// Chat overlay
const chatOverlay = document.getElementById("chatOverlay");
const closeChatOverlay = document.getElementById("closeChatOverlay");
const addPatientBtn = document.getElementById("addPatientBtn");
const patientList = document.getElementById("patientList");
const chatWindow = document.getElementById("chatWindow");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const sessionHeader = document.getElementById("sessionHeader");
const chatSearch = document.getElementById("chatSearch");

// Report overlay
const reportOverlay = document.getElementById("reportOverlay");
const closeReportOverlay = document.getElementById("closeReportOverlay");
const reportPatientList = document.getElementById("reportPatientList");
const reportEmptyState = document.getElementById("reportEmptyState");
const reportLoading = document.getElementById("reportLoading");
const reportContent = document.getElementById("reportContent");
const reportHeaderCard = document.getElementById("reportHeaderCard");
const reportStats = document.getElementById("reportStats");
const reportSessionsGrid = document.getElementById("reportSessionsGrid");
const reportAiAnalysis = document.getElementById("reportAiAnalysis");
const reportFooter = document.getElementById("reportFooter");

// Assessment modal
const assessmentModal = document.getElementById("assessmentModal");
const symptomInput = document.getElementById("symptomInput");
const assessmentResult = document.getElementById("assessmentResult");
const assessmentLoading = document.getElementById("assessmentLoading");

// Mood modal
const moodModal = document.getElementById("moodModal");
const moodPatientSelect = document.getElementById("moodPatientSelect");
const moodSlider = document.getElementById("moodSlider");
const moodScoreDisplay = document.getElementById("moodScoreDisplay");
const moodNote = document.getElementById("moodNote");
const moodHistory = document.getElementById("moodHistory");

// State
let patients = [];
let currentPatientId = null;
let currentSessionId = null;
let selectedReportPatientId = null;
let voiceEnabled = true;
let lastBotMessage = "";

// ==========================================
// API HELPERS
// ==========================================

async function apiGet(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) { console.error("API error:", res.status); return []; }
    return res.json();
  } catch (e) { console.error("Fetch error:", e); return []; }
}

async function apiPost(url, body) {
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();
    if (!res.ok) return { error: data.error || "Request failed" };
    return data;
  } catch (e) { console.error("Fetch error:", e); return { error: "Network error" }; }
}

function escapeHtml(str) {
  if (!str) return "";
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ==========================================
// HERO STATS
// ==========================================

async function loadHeroStats() {
  const data = await apiGet("/get_patients");
  const statPatients = document.getElementById("statPatients");
  const statSessions = document.getElementById("statSessions");
  const statMessages = document.getElementById("statMessages");

  let totalSessions = 0, totalMessages = 0;
  data.forEach(p => {
    totalSessions += p.sessions.length;
    p.sessions.forEach(s => { totalMessages += s.messages.length; });
  });

  animateCounter(statPatients, data.length);
  animateCounter(statSessions, totalSessions);
  animateCounter(statMessages, totalMessages);
}

function animateCounter(el, target) {
  if (!el) return;
  let current = 0;
  const step = Math.max(1, Math.ceil(target / 30));
  const timer = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = current;
  }, 40);
}

// ==========================================
// SPEECH
// ==========================================

const voiceToggle = document.getElementById("voiceToggle");

if (voiceToggle) {
  voiceToggle.onclick = () => {
    voiceEnabled = !voiceEnabled;
    if (voiceEnabled) {
      voiceToggle.classList.remove("off");
      if (lastBotMessage) speak(lastBotMessage);
    } else {
      voiceToggle.classList.add("off");
      speechSynthesis.cancel();
    }
  };
}

function speak(text) {
  if (!voiceEnabled || !window.speechSynthesis) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US"; u.rate = 1; u.pitch = 1;
  speechSynthesis.speak(u);
}

// Voice input
const voiceBtn = document.getElementById("voiceBtn");
if (voiceBtn) {
  voiceBtn.addEventListener("click", () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert("Voice recognition not supported"); return; }
    const r = new SR();
    r.lang = "en-US"; r.interimResults = false;
    r.start();
    r.onresult = (e) => { userInput.value = e.results[0][0].transcript; };
  });
}

// ==========================================
// CHAT OVERLAY — OPEN / CLOSE
// ==========================================

function openChatScreen() {
  chatOverlay.classList.remove("hidden");
  document.body.classList.add("chat-open");
  loadPatients();
}

function closeChatScreen() {
  chatOverlay.classList.add("hidden");
  document.body.classList.remove("chat-open");
  document.querySelectorAll(".menu-box").forEach(m => m.classList.remove("show"));
}

document.getElementById("openChatNav")?.addEventListener("click", openChatScreen);
document.getElementById("openChatCard")?.addEventListener("click", openChatScreen);
document.getElementById("openChatFeature")?.addEventListener("click", openChatScreen);
closeChatOverlay?.addEventListener("click", closeChatScreen);

// ==========================================
// PATIENTS
// ==========================================

async function loadPatients() {
  patients = await apiGet("/get_patients");
  renderPatients(patients);
}

function renderPatients(data) {
  patientList.innerHTML = "";
  data.forEach(patient => {
    const card = document.createElement("div");
    card.className = "patient-card";

    const top = document.createElement("div");
    top.className = "patient-top";

    const hoverArea = document.createElement("div");
    hoverArea.className = "patient-hover-area";

    const nameEl = document.createElement("div");
    nameEl.className = "patient-name";
    nameEl.textContent = patient.name;

    const dropdown = document.createElement("div");
    dropdown.className = "patient-hover-dropdown";

    nameEl.onclick = (e) => {
      e.stopPropagation();
      document.querySelectorAll(".patient-hover-dropdown").forEach(d => {
        if (d !== dropdown) d.classList.remove("show");
      });
      dropdown.classList.toggle("show");
    };

    const menuWrap = createMenu([
      {
        label: "Rename",
        action: async () => {
          const n = prompt("Rename patient", patient.name);
          if (!n) return;
          await apiPost("/rename_patient", { patient_id: patient.id, name: n });
          loadPatients();
        }
      },
      {
        label: "Delete",
        action: async () => {
          if (!confirm(`Delete ${patient.name}?`)) return;
          await apiPost("/delete_patient", { patient_id: patient.id });
          if (currentPatientId === patient.id) { currentPatientId = null; currentSessionId = null; clearChatArea(); }
          loadPatients();
        }
      },
      {
        label: "New Session",
        action: async () => {
          const n = prompt("Session name");
          await apiPost("/add_session", { patient_id: patient.id, name: n || "" });
          loadPatients();
        }
      }
    ]);

    if (patient.sessions.length === 0) {
      const empty = document.createElement("div");
      empty.className = "session-empty";
      empty.textContent = "No sessions yet";
      dropdown.appendChild(empty);
    } else {
      patient.sessions.forEach(session => {
        const item = document.createElement("div");
        item.className = "hover-session-item";
        item.onclick = () => { openSession(patient.id, session.id); dropdown.classList.remove("show"); };

        const title = document.createElement("div");
        title.className = "hover-session-title";
        title.textContent = session.name;

        const meta = document.createElement("div");
        meta.className = "hover-session-meta";
        meta.textContent = `Created: ${session.created_at || "N/A"}`;

        item.appendChild(title);
        item.appendChild(meta);
        dropdown.appendChild(item);
      });
    }

    hoverArea.appendChild(nameEl);
    hoverArea.appendChild(dropdown);
    top.appendChild(hoverArea);
    top.appendChild(menuWrap);
    card.appendChild(top);
    patientList.appendChild(card);
  });
}

function createMenu(items) {
  const wrap = document.createElement("div");
  wrap.className = "menu-wrap";

  const btn = document.createElement("button");
  btn.className = "menu-btn";
  btn.textContent = "\u22EE";

  const box = document.createElement("div");
  box.className = "menu-box";

  items.forEach(item => {
    const mi = document.createElement("button");
    mi.textContent = item.label;
    mi.onclick = async (e) => { e.stopPropagation(); box.classList.remove("show"); await item.action(); };
    box.appendChild(mi);
  });

  btn.onclick = (e) => {
    e.stopPropagation();
    document.querySelectorAll(".menu-box").forEach(m => { if (m !== box) m.classList.remove("show"); });
    box.classList.toggle("show");
  };

  wrap.appendChild(btn);
  wrap.appendChild(box);
  return wrap;
}

// Close menus on click outside
document.addEventListener("click", () => {
  document.querySelectorAll(".menu-box").forEach(m => m.classList.remove("show"));
  document.querySelectorAll(".patient-hover-dropdown").forEach(d => d.classList.remove("show"));
});

// ==========================================
// SESSION
// ==========================================

function openSession(patientId, sessionId) {
  currentPatientId = patientId;
  currentSessionId = sessionId;
  const patient = patients.find(p => p.id === patientId);
  if (!patient) return;
  const session = patient.sessions.find(s => s.id === sessionId);
  if (!session) return;
  sessionHeader.innerHTML = `<h2>${escapeHtml(patient.name)}</h2><p>${escapeHtml(session.name)}</p>`;
  chatWindow.innerHTML = "";
  session.messages.forEach(msg => appendMessage(msg.type, msg.text));
}

function clearChatArea() {
  sessionHeader.innerHTML = `<h2>Select a patient and session</h2><p>Start a new patient or open an existing session.</p>`;
  chatWindow.innerHTML = "";
}

function appendMessage(type, text) {
  const div = document.createElement("div");
  div.className = type === "user" ? "user-msg" : "bot-msg";
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ==========================================
// ADD PATIENT
// ==========================================

if (addPatientBtn) {
  addPatientBtn.addEventListener("click", async () => {
    const n = prompt("Patient name");
    await apiPost("/add_patient", { name: n || "" });
    loadPatients();
  });
}

// ==========================================
// SEND MESSAGE
// ==========================================

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  if (!currentPatientId || !currentSessionId) { alert("Please select a patient and session first."); return; }

  appendMessage("user", message);
  userInput.value = "";

  const thinking = document.createElement("div");
  thinking.className = "bot-msg";
  thinking.textContent = "MindSync is thinking...";
  chatWindow.appendChild(thinking);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  try {
    const response = await apiPost("/chat", {
      patient_id: currentPatientId,
      session_id: currentSessionId,
      message: message
    });

    if (response.error) {
      thinking.textContent = response.error;
    } else {
      thinking.textContent = response.response;
      lastBotMessage = response.response;
      speak(lastBotMessage);
    }
  } catch (err) {
    thinking.textContent = "Error connecting to MindSync AI.";
  }

  loadPatients();
}

sendBtn?.addEventListener("click", sendMessage);
userInput?.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });

// ==========================================
// SEARCH
// ==========================================

if (chatSearch) {
  chatSearch.addEventListener("input", () => {
    const kw = chatSearch.value.trim().toLowerCase();
    if (!kw) { renderPatients(patients); return; }
    const filtered = patients.map(p => {
      const pMatch = p.name.toLowerCase().includes(kw);
      const sMatched = p.sessions.filter(s =>
        s.name.toLowerCase().includes(kw) ||
        s.messages.some(m => m.text.toLowerCase().includes(kw))
      );
      if (pMatch || sMatched.length > 0) return { ...p, sessions: pMatch ? p.sessions : sMatched };
      return null;
    }).filter(Boolean);
    renderPatients(filtered);
  });
}

// ==========================================
// REPORT OVERLAY
// ==========================================

function openReportScreen() {
  reportOverlay.classList.remove("hidden");
  document.body.classList.add("chat-open");
  loadReportPatients();
}

function closeReportScreen() {
  reportOverlay.classList.add("hidden");
  document.body.classList.remove("chat-open");
  selectedReportPatientId = null;
  showReportEmpty();
}

document.getElementById("openReportBtn")?.addEventListener("click", openReportScreen);
document.getElementById("openReportFeature")?.addEventListener("click", openReportScreen);
closeReportOverlay?.addEventListener("click", closeReportScreen);

async function loadReportPatients() {
  const data = await apiGet("/get_patients");
  renderReportPatients(data);
}

function renderReportPatients(data) {
  reportPatientList.innerHTML = "";
  if (data.length === 0) {
    reportPatientList.innerHTML = `<div class="report-no-patients">No patients found. Add patients through the chat first.</div>`;
    return;
  }
  data.forEach(patient => {
    const totalMsgs = patient.sessions.reduce((sum, s) => sum + s.messages.length, 0);
    const card = document.createElement("div");
    card.className = "report-patient-card";
    if (patient.id === selectedReportPatientId) card.classList.add("active");
    card.innerHTML = `
      <div class="report-patient-name">${escapeHtml(patient.name)}</div>
      <div class="report-patient-meta">
        <span>${patient.sessions.length} session${patient.sessions.length !== 1 ? "s" : ""}</span>
        <span>${totalMsgs} message${totalMsgs !== 1 ? "s" : ""}</span>
      </div>
    `;
    card.addEventListener("click", () => {
      selectedReportPatientId = patient.id;
      document.querySelectorAll(".report-patient-card").forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      generateReport(patient.id);
    });
    reportPatientList.appendChild(card);
  });
}

function showReportEmpty() {
  reportEmptyState.classList.remove("hidden");
  reportLoading.classList.add("hidden");
  reportContent.classList.add("hidden");
}

function showReportLoading() {
  reportEmptyState.classList.add("hidden");
  reportLoading.classList.remove("hidden");
  reportContent.classList.add("hidden");
}

function showReportContent() {
  reportEmptyState.classList.add("hidden");
  reportLoading.classList.add("hidden");
  reportContent.classList.remove("hidden");
}

async function generateReport(patientId) {
  showReportLoading();
  try {
    const report = await apiPost("/generate_report", { patient_id: patientId });
    if (report.error) {
      showReportEmpty();
      reportEmptyState.innerHTML = `
        <div class="report-empty-icon"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg></div>
        <h2>Cannot Generate Report</h2>
        <p>${escapeHtml(report.error)}</p>
      `;
      return;
    }
    renderReport(report);
    showReportContent();
  } catch (err) {
    console.error("Report error:", err);
    showReportEmpty();
    reportEmptyState.innerHTML = `
      <div class="report-empty-icon"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg></div>
      <h2>Error</h2>
      <p>Failed to generate report. Please try again.</p>
    `;
  }
}

function renderReport(report) {
  // Header
  const patientInfo = [];
  if (report.patient_age && report.patient_age !== "N/A") patientInfo.push(`Age: ${escapeHtml(report.patient_age)}`);
  if (report.patient_gender && report.patient_gender !== "N/A") patientInfo.push(`Gender: ${escapeHtml(report.patient_gender)}`);

  reportHeaderCard.innerHTML = `
    <div class="report-title-row">
      <div>
        <h2>Clinical Report: ${escapeHtml(report.patient_name)}</h2>
        ${patientInfo.length ? `<div class="report-patient-info">${patientInfo.map(i => `<span>${i}</span>`).join("")}</div>` : ""}
      </div>
      <span class="report-timestamp">Generated: ${escapeHtml(report.generated_at)}</span>
    </div>
  `;

  // Stats
  const avg = report.total_sessions > 0 ? Math.round(report.total_messages / report.total_sessions) : 0;
  reportStats.innerHTML = `
    <div class="stat-card"><div class="stat-value">${report.total_sessions}</div><div class="stat-label">Total Sessions</div></div>
    <div class="stat-card"><div class="stat-value">${report.total_messages}</div><div class="stat-label">Total Messages</div></div>
    <div class="stat-card"><div class="stat-value">${avg}</div><div class="stat-label">Avg Msgs/Session</div></div>
  `;

  // Sessions
  let sessHtml = `<h3 class="report-section-title">Session Breakdown</h3><div class="session-cards">`;
  report.sessions.forEach(s => {
    sessHtml += `
      <div class="report-session-card">
        <div class="report-session-name">${escapeHtml(s.name)}</div>
        <div class="report-session-detail">
          <span>${escapeHtml(s.created_at)}</span>
          <span>${s.message_count} messages</span>
        </div>
      </div>
    `;
  });
  sessHtml += `</div>`;
  reportSessionsGrid.innerHTML = sessHtml;

  // AI Analysis
  reportAiAnalysis.innerHTML = `
    <h3 class="report-section-title">AI Analysis</h3>
    <div class="analysis-content">${formatAnalysis(report.ai_analysis)}</div>
  `;

  // Footer
  reportFooter.innerHTML = `
    <p>Report generated by MindSync AI — ${escapeHtml(report.generated_at)}</p>
    <button class="report-print-btn" onclick="printReport()">Print Report</button>
  `;
}

function formatAnalysis(text) {
  if (!text) return "<p>No analysis available.</p>";
  let s = escapeHtml(text);
  s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  s = s.replace(/^(\d+\.\s*)(<strong>.*?<\/strong>)/gm, '<h4 class="analysis-heading">$1$2</h4>');
  s = s.replace(/^[\-\*]\s+(.+)$/gm, "<li>$1</li>");
  s = s.replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");
  s = s.replace(/<\/ul>\s*<ul>/g, "");
  s = s.replace(/\n\n/g, "</p><p>");
  s = s.replace(/\n/g, "<br>");
  return `<p>${s}</p>`;
}

function printReport() {
  const content = reportContent.innerHTML;
  const w = window.open("", "_blank");
  w.document.write(`<html><head><title>MindSync AI — Patient Report</title><style>
    body{font-family:'Inter',Arial,sans-serif;padding:40px;color:#1a1a1a;max-width:900px;margin:0 auto}
    h2{color:#0a1324;margin-bottom:8px}h3{color:#16233a;margin:24px 0 12px}
    h4{color:#22314d;margin:16px 0 8px}
    .stat-card{display:inline-block;padding:16px 24px;margin:8px;border:1px solid #ddd;border-radius:12px;text-align:center}
    .stat-value{font-size:28px;font-weight:700;color:#0a1324}.stat-label{font-size:13px;color:#666;margin-top:4px}
    .report-session-card{padding:12px;border:1px solid #ddd;border-radius:10px;margin:8px 0}
    .report-session-name{font-weight:600}.report-session-detail{color:#666;font-size:13px;margin-top:4px}
    .report-session-detail span{margin-right:16px}.analysis-content{line-height:1.8}
    .report-print-btn{display:none}.report-timestamp{color:#666;font-size:14px}
    ul{padding-left:20px}li{margin:4px 0}strong{color:#0a1324}
  </style></head><body>${content}</body></html>`);
  w.document.close();
  w.print();
}

// ==========================================
// ASSESSMENT MODAL
// ==========================================

document.getElementById("openAssessmentBtn")?.addEventListener("click", () => {
  assessmentModal.classList.remove("hidden");
  assessmentResult.classList.add("hidden");
  assessmentLoading.classList.add("hidden");
  if (symptomInput) symptomInput.value = "";
});

document.getElementById("closeAssessment")?.addEventListener("click", () => {
  assessmentModal.classList.add("hidden");
});

document.getElementById("submitAssessment")?.addEventListener("click", async () => {
  const symptoms = symptomInput?.value.trim();
  if (!symptoms) { alert("Please describe your symptoms."); return; }

  assessmentResult.classList.add("hidden");
  assessmentLoading.classList.remove("hidden");

  const res = await apiPost("/health_assessment", { symptoms });

  assessmentLoading.classList.add("hidden");

  if (res.error) {
    assessmentResult.innerHTML = `<strong>Error:</strong> ${escapeHtml(res.error)}`;
  } else {
    assessmentResult.innerHTML = formatAnalysis(res.assessment);
  }
  assessmentResult.classList.remove("hidden");
});

// ==========================================
// MOOD MODAL
// ==========================================

document.getElementById("openMoodBtn")?.addEventListener("click", async () => {
  moodModal.classList.remove("hidden");
  // Load patients into select
  const data = await apiGet("/get_patients");
  moodPatientSelect.innerHTML = `<option value="">Select Patient</option>`;
  data.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.name;
    moodPatientSelect.appendChild(opt);
  });
  moodHistory.innerHTML = "";
  if (moodNote) moodNote.value = "";
  if (moodSlider) { moodSlider.value = 5; moodScoreDisplay.textContent = "5"; }
});

document.getElementById("closeMood")?.addEventListener("click", () => {
  moodModal.classList.add("hidden");
});

if (moodSlider) {
  moodSlider.addEventListener("input", () => {
    moodScoreDisplay.textContent = moodSlider.value;
  });
}

// Load mood history when patient selected
if (moodPatientSelect) {
  moodPatientSelect.addEventListener("change", async () => {
    const pid = moodPatientSelect.value;
    if (!pid) { moodHistory.innerHTML = ""; return; }
    const logs = await apiPost("/get_mood_logs", { patient_id: pid });
    renderMoodHistory(Array.isArray(logs) ? logs : []);
  });
}

document.getElementById("submitMood")?.addEventListener("click", async () => {
  const pid = moodPatientSelect?.value;
  if (!pid) { alert("Please select a patient."); return; }

  const score = parseInt(moodSlider?.value || "5");
  const note = moodNote?.value.trim() || "";

  const res = await apiPost("/log_mood", { patient_id: pid, mood_score: score, note });
  if (res.error) { alert(res.error); return; }

  // Refresh history
  const logs = await apiPost("/get_mood_logs", { patient_id: pid });
  renderMoodHistory(Array.isArray(logs) ? logs : []);
  if (moodNote) moodNote.value = "";
});

function renderMoodHistory(logs) {
  if (!moodHistory) return;
  if (logs.length === 0) {
    moodHistory.innerHTML = `<p style="color:var(--muted-2);text-align:center;font-size:13px;padding:12px 0;">No mood entries yet.</p>`;
    return;
  }
  moodHistory.innerHTML = logs.slice().reverse().map(log => {
    const scoreClass = log.score <= 3 ? "mood-score-low" : log.score <= 6 ? "mood-score-mid" : "mood-score-high";
    return `
      <div class="mood-entry">
        <div class="mood-score-badge ${scoreClass}">${log.score}</div>
        <div class="mood-entry-details">
          <div class="mood-entry-note">${escapeHtml(log.note) || "No note"}</div>
          <div class="mood-entry-time">${escapeHtml(log.timestamp)}</div>
        </div>
      </div>
    `;
  }).join("");
}
