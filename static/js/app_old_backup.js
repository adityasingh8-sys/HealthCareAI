/*class ElectronApp {
    constructor() {
        this.recognition = null;
        this.speechSynth = window.speechSynthesis;
        this.voiceEnabled = true;
        this.initSpeechRecognition();
        this.setupEventListeners();
    }

    initSpeechRecognition() {
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.lang = 'en-US';

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.handleUserInput(transcript);
            };

            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.toggleLoading(false);
            };
        }
    }

    setupEventListeners() {
        document.getElementById('userInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    async sendMessage() {
        const input = document.getElementById('userInput');
        const text = input.value.trim();
        if (!text) return;
        input.value = '';
        this.handleUserInput(text);
    }

    async handleUserInput(text) {
        this.addMessage(text, 'user');
        this.toggleLoading(true);
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            this.addMessage(data.response, 'bot');
            if (this.voiceEnabled) this.speak(data.response);
        } catch (error) {
            console.error('Fetch error:', error);
            this.addMessage("An error occurred while contacting Electron.", 'bot');
        } finally {
            this.toggleLoading(false);
        }
    }

    addMessage(text, sender) {
        const history = document.getElementById('chatHistory');
        const msg = document.createElement('div');
        msg.className = `message ${sender}`;
        msg.textContent = text;
        history.appendChild(msg);
        history.scrollTop = history.scrollHeight;
    }

    speak(text) {
        if (this.speechSynth.speaking) return;
        const utterance = new SpeechSynthesisUtterance(text);
        this.speechSynth.speak(utterance);
    }

    toggleLoading(state) {
        const loading = document.getElementById('loading');
        loading.classList.toggle('hidden', !state);
    }

    startListening() {
        if (this.recognition) this.recognition.start();
    }

    toggleVoice() {
        this.voiceEnabled = !this.voiceEnabled;
        alert(`Voice output ${this.voiceEnabled ? "enabled" : "disabled"}`);
    }
}

const app = new ElectronApp();

function sendMessage() {
    app.sendMessage();
}

function startListening() {
    app.startListening();
}

function toggleVoice() {
    app.toggleVoice();
}*/
// ---------------- LOADING SCREEN ----------------
// ---------------- LOADING SCREEN ----------------
// stop any ongoing speech on page load

/*let voiceEnabled = true;

const voiceToggle = document.getElementById("voiceToggle");

if(voiceToggle){

voiceToggle.addEventListener("click", () => {

voiceEnabled = !voiceEnabled;

if(voiceEnabled){
voiceToggle.innerText = "🔊 Electron Voice ON";
}else{
voiceToggle.innerText = "🔇 Electron Voice OFF";
speechSynthesis.cancel();
}

});

}

window.addEventListener("load", () => {
    if ("speechSynthesis" in window) {
        speechSynthesis.cancel();
    }
});

document.documentElement.classList.add("loading")
document.body.classList.add("loading")
const lines = [
"INITIALIZING Electron...",
"LOADING NEURAL NETWORK...",
"CONNECTING AI CORE...",
"STARTING SYSTEM...",
"READY"
]

let i = 0
const text = document.getElementById("loadingText")

function changeText(){

if(!text) return

text.innerText = lines[i]

i++

if(i < lines.length){
setTimeout(changeText,1200)
}else{
setTimeout(showLandingPage,1000)
}

}

function showLandingPage(){

const loading = document.getElementById("loading-screen")
const landing = document.getElementById("landing-page")

if(loading) loading.style.display = "none"
if(landing) landing.classList.remove("hidden")

document.documentElement.classList.remove("loading")
document.body.classList.remove("loading")

}

changeText()



// ---------------- CHAT ELEMENTS ----------------

const chatWindow = document.getElementById("chatWindow")
const input = document.querySelector(".chat-input input")
const newChatBtn = document.querySelector(".new-chat")
const chatHistory = document.querySelector(".chat-history")
const voiceBtn = document.querySelector(".voice-btn")

let currentChat = null



// ---------------- LOAD CHATS FROM SERVER ----------------

async function loadChats(){

const res = await fetch("/get_chats")

const chats = await res.json()

renderChatHistory(chats)

if(chats.length > 0){
loadChat(chats[chats.length-1])
}

}



// ---------------- DISPLAY CHAT HISTORY ----------------

function renderChatHistory(chats){

if(!chatHistory) return

chatHistory.innerHTML = "<h3>Saved Chats</h3>"

chats.forEach(chat => {

const item = document.createElement("div")

item.className = "chat-item"

item.innerText = chat.title || ("Chat " + chat.id)

item.onclick = () => loadChat(chat)

chatHistory.appendChild(item)

})

}



// ---------------- LOAD CHAT ----------------

function loadChat(chat){

currentChat = chat

chatWindow.innerHTML = ""

chat.messages.forEach(msg => {

const div = document.createElement("div")

div.className = msg.type === "user" ? "user-msg" : "bot-msg"

div.innerText = msg.text

chatWindow.appendChild(div)

})

}



// ---------------- CREATE NEW CHAT ----------------

if(newChatBtn){

newChatBtn.addEventListener("click", createNewChat)

}

async function createNewChat(){

const res = await fetch("/new_chat",{
method:"POST"
})

const chat = await res.json()

loadChats()

loadChat(chat)

}



// ---------------- SEND MESSAGE ----------------

async function sendMessage(){

const message = input.value.trim()

if(!message || !currentChat) return


// USER MESSAGE

const userDiv = document.createElement("div")
userDiv.className = "user-msg"
userDiv.innerText = message

chatWindow.appendChild(userDiv)

input.value = ""


// SAVE USER MESSAGE

await fetch("/save_message", {
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
chat_id: String(currentChat.id),
message:{
type:"user",
text:message
}
})
})


// BOT PLACEHOLDER

const botDiv = document.createElement("div")
botDiv.className = "bot-msg"
botDiv.innerText = "Electron is thinking..."

chatWindow.appendChild(botDiv)



try{

const response = await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
message: message
})

})

const data = await response.json()

botDiv.innerText = data.response

speakElectron(data.response)


// SAVE BOT MESSAGE

await fetch("/save_message", {
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
chat_id: String(currentChat.id),
message:{
type:"bot",
text:data.response
}
})
})

}catch(error){

botDiv.innerText = "Error connecting to Electron."

console.error(error)

}

}



// ---------------- ENTER KEY SEND ----------------

if(input){
input.addEventListener("keypress", e => {

if(e.key === "Enter"){
sendMessage()
}

})
}



// ---------------- VOICE INPUT ----------------

if(voiceBtn){

voiceBtn.addEventListener("click", () => {

const SpeechRecognition =
window.SpeechRecognition || window.webkitSpeechRecognition

if(!SpeechRecognition){
alert("Voice recognition not supported in this browser")
return
}

const recognition = new SpeechRecognition()

recognition.lang = "en-US"

recognition.start()

recognition.onresult = (event)=>{

const transcript = event.results[0][0].transcript

input.value = transcript

}

})

}



// ---------------- DELETE CHAT ----------------

async function deleteChat(chat_id){

await fetch("/delete_chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({chat_id})

})

loadChats()

}



// ---------------- RENAME CHAT ----------------

async function renameChat(chat_id){

let newName = prompt("Enter new chat name")

if(!newName) return

await fetch("/rename_chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
chat_id: chat_id,
title: newName
})

})

loadChats()

}



// ---------------- INITIAL LOAD ----------------

loadChats()

function speakElectron(text){

if(!voiceEnabled) return;

if(!("speechSynthesis" in window)) return;

speechSynthesis.cancel();

const speech = new SpeechSynthesisUtterance(text);

speech.lang = "en-US";
speech.rate = 1;
speech.pitch = 1;

speechSynthesis.speak(speech);

}*/


window.speechSynthesis.cancel()
const openChatNav = document.getElementById("openChatNav");
const openChatCard = document.getElementById("openChatCard");
const chatOverlay = document.getElementById("chatOverlay");
const closeChatOverlay = document.getElementById("closeChatOverlay");
const addPatientBtn = document.getElementById("addPatientBtn");
const patientList = document.getElementById("patientList");
const chatWindow = document.getElementById("chatWindow");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const sessionHeader = document.getElementById("sessionHeader");
const chatSearch = document.getElementById("chatSearch");

document.documentElement.classList.add("loading")
document.body.classList.add("loading")
const lines = [
"INITIALIZING Electron...",
"LOADING NEURAL NETWORK...",
"CONNECTING AI CORE...",
"STARTING SYSTEM...",
"READY"
]

let i = 0
const text = document.getElementById("loadingText")

function changeText(){

if(!text) return

text.innerText = lines[i]

i++

if(i < lines.length){
setTimeout(changeText,1200)
}else{
setTimeout(showLandingPage,1000)
}

}

function showLandingPage(){

const loading = document.getElementById("loading-screen")
const landing = document.getElementById("landing-page")

if(loading) loading.style.display = "none"
if(landing) landing.classList.remove("hidden")

document.documentElement.classList.remove("loading")
document.body.classList.remove("loading")

}

changeText()

let patients = [];
let currentPatientId = null;
let currentSessionId = null;


// ---------- OPEN / CLOSE OVERLAY ----------

function openChatScreen(){
  chatOverlay.classList.remove("hidden");
  document.body.classList.add("chat-open");
  loadPatients();
}

function closeChatScreen(){
  chatOverlay.classList.add("hidden");
  document.body.classList.remove("chat-open");
   document.querySelectorAll(".menu-box").forEach(m => m.classList.remove("show"));
}

if (openChatNav) openChatNav.addEventListener("click", openChatScreen);
if (openChatCard) openChatCard.addEventListener("click", openChatScreen);
if (closeChatOverlay) closeChatOverlay.addEventListener("click", closeChatScreen);

let voiceEnabled = true
let lastBotMessage = ""

const voiceToggle = document.getElementById("voiceToggle")

if(voiceToggle){

  voiceToggle.onclick = ()=>{

    voiceEnabled = !voiceEnabled

    if(voiceEnabled){

      voiceToggle.textContent = "🔊"
      voiceToggle.classList.remove("off")

      // speak the last message if it exists
      if(lastBotMessage){
        speak(lastBotMessage)
      }

    }else{

      voiceToggle.textContent = "🔇"
      voiceToggle.classList.add("off")

      // stop speaking immediately
      speechSynthesis.cancel()

    }

  }

}

function speak(text){

  if(!voiceEnabled) return

  if(!window.speechSynthesis) return

  const speech = new SpeechSynthesisUtterance(text)

  speech.lang = "en-US"
  speech.rate = 1
  speech.pitch = 1

  speechSynthesis.speak(speech)

}
// ---------- API ----------

async function apiGet(url){
  const res = await fetch(url);
  if(!res.ok){
    console.error("API error:", res.status);
    return [];
  }
  return res.json();
}

async function apiPost(url, body){
  const res = await fetch(url,{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify(body)
  });

  if(!res.ok){
    console.error("API error:", res.status);
    return {};
  }

  return res.json();
}

// ---------- LOAD / RENDER ----------

async function loadPatients(){
  patients = await apiGet("/get_patients");
  renderPatients(patients);
}

function renderPatients(data){
  patientList.innerHTML = "";

  data.forEach(patient => {
    const patientCard = document.createElement("div");
    patientCard.className = "patient-card";

    const patientTop = document.createElement("div");
    patientTop.className = "patient-top";

    const patientHoverArea = document.createElement("div");
    patientHoverArea.className = "patient-hover-area";

    const patientName = document.createElement("div");
    patientName.className = "patient-name";
    patientName.textContent = patient.name;

    const hoverDropdown = document.createElement("div");
    hoverDropdown.className = "patient-hover-dropdown";

    patientName.onclick = (e)=>{
      e.stopPropagation();

      document.querySelectorAll(".patient-hover-dropdown").forEach(d=>{
        if(d !== hoverDropdown) d.classList.remove("show");
      });

      hoverDropdown.classList.toggle("show");
    };

    const patientMenuWrap = createMenu([
      {
        label: "Rename",
        action: async () => {
          const newName = prompt("Rename patient", patient.name);
          if(!newName) return;
          await apiPost("/rename_patient", {
            patient_id: patient.id,
            name: newName
          });
          loadPatients();
        }
      },
      {
        label: "Delete",
        action: async () => {
          if(!confirm(`Delete ${patient.name}?`)) return;
          await apiPost("/delete_patient", { patient_id: patient.id });

          if(currentPatientId === patient.id){
            currentPatientId = null;
            currentSessionId = null;
            clearChatArea();
          }

          loadPatients();
        }
      },
      {
        label: "New Session",
        action: async () => {
          const sessionName = prompt("Session name");
          await apiPost("/add_session", {
            patient_id: patient.id,
            name: sessionName || ""
          });
          loadPatients();
        }
      }
    ]);

    if(patient.sessions.length === 0){
      const emptyText = document.createElement("div");
      emptyText.className = "session-empty";
      emptyText.textContent = "No sessions yet";
      hoverDropdown.appendChild(emptyText);
    } else {
      patient.sessions.forEach(session => {
        const sessionItem = document.createElement("div");
        sessionItem.className = "hover-session-item";

        sessionItem.onclick = () => {
          openSession(patient.id, session.id);
          hoverDropdown.classList.remove("show");
        };

        const sessionTitle = document.createElement("div");
        sessionTitle.className = "hover-session-title";
        sessionTitle.textContent = session.name;

        const sessionMeta = document.createElement("div");
        sessionMeta.className = "hover-session-meta";
        sessionMeta.textContent = `(Created on: ${session.created_at || "N/A"})`;

        sessionItem.appendChild(sessionTitle);
        sessionItem.appendChild(sessionMeta);
        hoverDropdown.appendChild(sessionItem);
      });
    }

    patientHoverArea.appendChild(patientName);
    patientHoverArea.appendChild(hoverDropdown);

    patientTop.appendChild(patientHoverArea);
    patientTop.appendChild(patientMenuWrap);
    patientCard.appendChild(patientTop);

    patientList.appendChild(patientCard);
  });
}
function createMenu(items){
  const wrap = document.createElement("div");
  wrap.className = "menu-wrap";

  const btn = document.createElement("button");
  btn.className = "menu-btn";
  btn.textContent = "⋮";

  const box = document.createElement("div");
  box.className = "menu-box";

  items.forEach(item => {
    const menuItem = document.createElement("button");
    menuItem.textContent = item.label;
    menuItem.onclick = async (e) => {
      e.stopPropagation();
      box.classList.remove("show");
      await item.action();
    };
    box.appendChild(menuItem);
  });

  btn.onclick = (e) => {
    e.stopPropagation();
    document.querySelectorAll(".menu-box").forEach(m => {
      if (m !== box) m.classList.remove("show");
    });
    box.classList.toggle("show");
  };

  wrap.appendChild(btn);
  wrap.appendChild(box);
  return wrap;
}

document.addEventListener("click", () => {
  document.querySelectorAll(".menu-box").forEach(m => m.classList.remove("show"));
  document.querySelectorAll(".patient-hover-dropdown").forEach(d => d.classList.remove("show"));
});


// ---------- SESSION ----------

function openSession(patientId, sessionId){

  currentPatientId = patientId;
  currentSessionId = sessionId;

  const patient = patients.find(p => p.id === patientId);

  if(!patient){
    console.error("Patient not found");
    return;
  }

  const session = patient.sessions.find(s => s.id === sessionId);

  if(!session){
    console.error("Session not found");
    return;
  }

  sessionHeader.innerHTML = `
    <h2>${patient.name}</h2>
    <p>${session.name}</p>
  `;

  chatWindow.innerHTML = "";

  session.messages.forEach(msg=>{
    appendMessage(msg.type,msg.text);
  });

}

function clearChatArea(){
  sessionHeader.innerHTML = `
    <h2>Select a patient and session</h2>
    <p>Start a new patient or open an existing session.</p>
  `;
  chatWindow.innerHTML = "";
}

function appendMessage(type,text){

  const div = document.createElement("div");

  div.className = type === "user" ? "user-msg" : "bot-msg";

  div.textContent = text;

  chatWindow.appendChild(div);

  chatWindow.scrollTop = chatWindow.scrollHeight;

}


// ---------- ADD PATIENT ----------

if (addPatientBtn){
  addPatientBtn.addEventListener("click", async () => {
    const patientName = prompt("Patient name");
    await apiPost("/add_patient", { name: patientName || "" });
    loadPatients();
  });
}


// ---------- SEND MESSAGE ----------

async function sendMessage(){

  const message = userInput.value.trim();

  if(!message){
    return;
  }

  if(!currentPatientId || !currentSessionId){
    alert("Please select a patient and session first.");
    return;
  }

  appendMessage("user",message);

  userInput.value = "";

  const thinkingDiv = document.createElement("div");
  thinkingDiv.className = "bot-msg";
  thinkingDiv.textContent = "Electron is thinking...";
  chatWindow.appendChild(thinkingDiv);

  chatWindow.scrollTop = chatWindow.scrollHeight;

  try{

    const response = await apiPost("/chat",{
      patient_id: currentPatientId,
      session_id: currentSessionId,
      message: message
    });

    thinkingDiv.textContent = response.response;
    speak(lastBotMessage)

  }catch(err){

    thinkingDiv.textContent = "Error connecting to Electron.";

  }

  loadPatients();

}

if (sendBtn) sendBtn.addEventListener("click", sendMessage);

if (userInput){
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
}


// ---------- SEARCH ----------

if(chatSearch){

  chatSearch.addEventListener("input",()=>{

    const keyword = chatSearch.value.trim().toLowerCase();

    if(!keyword){
      renderPatients(patients);
      return;
    }

    const filtered = patients.map(patient=>{

      const patientMatch = patient.name.toLowerCase().includes(keyword);

      const matchedSessions = patient.sessions.filter(session=>{

        const sessionMatch = session.name.toLowerCase().includes(keyword);

        const messageMatch = session.messages.some(msg=>
          msg.text.toLowerCase().includes(keyword)
        );

        return sessionMatch || messageMatch;

      });

      if(patientMatch || matchedSessions.length > 0){

        return {
          ...patient,
          sessions: patientMatch ? patient.sessions : matchedSessions
        };

      }

      return null;

    }).filter(Boolean);

    renderPatients(filtered);

  });

}


// ---------- VOICE INPUT ----------

const voiceBtn = document.getElementById("voiceBtn");

if(voiceBtn){

  voiceBtn.addEventListener("click",()=>{

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if(!SpeechRecognition){
      alert("Voice recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult=(event)=>{

      const transcript = event.results[0][0].transcript;

      userInput.value = transcript;

    };

  });

}


// ========================================
// REPORT ANALYSIS
// ========================================

const openReportBtn = document.getElementById("openReportBtn");
const reportOverlay = document.getElementById("reportOverlay");
const closeReportOverlay = document.getElementById("closeReportOverlay");
const reportPatientList = document.getElementById("reportPatientList");
const reportDisplay = document.getElementById("reportDisplay");
const reportEmptyState = document.getElementById("reportEmptyState");
const reportLoading = document.getElementById("reportLoading");
const reportContent = document.getElementById("reportContent");
const reportHeaderCard = document.getElementById("reportHeaderCard");
const reportStats = document.getElementById("reportStats");
const reportSessionsGrid = document.getElementById("reportSessionsGrid");
const reportAiAnalysis = document.getElementById("reportAiAnalysis");
const reportFooter = document.getElementById("reportFooter");

let selectedReportPatientId = null;

function openReportScreen(){
  reportOverlay.classList.remove("hidden");
  document.body.classList.add("chat-open");
  loadReportPatients();
}

function closeReportScreen(){
  reportOverlay.classList.add("hidden");
  document.body.classList.remove("chat-open");
  selectedReportPatientId = null;
  showReportEmpty();
}

if(openReportBtn) openReportBtn.addEventListener("click", openReportScreen);
if(closeReportOverlay) closeReportOverlay.addEventListener("click", closeReportScreen);

async function loadReportPatients(){
  const data = await apiGet("/get_patients");
  renderReportPatients(data);
}

function renderReportPatients(data){
  reportPatientList.innerHTML = "";

  if(data.length === 0){
    reportPatientList.innerHTML = `<div class="report-no-patients">No patients found. Add patients through the chat first.</div>`;
    return;
  }

  data.forEach(patient => {
    const totalMsgs = patient.sessions.reduce((sum, s) => sum + s.messages.length, 0);
    const card = document.createElement("div");
    card.className = "report-patient-card";
    if(patient.id === selectedReportPatientId) card.classList.add("active");

    card.innerHTML = `
      <div class="report-patient-name">${escapeHtml(patient.name)}</div>
      <div class="report-patient-meta">
        <span>${patient.sessions.length} session${patient.sessions.length !== 1 ? 's' : ''}</span>
        <span>${totalMsgs} message${totalMsgs !== 1 ? 's' : ''}</span>
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

function escapeHtml(str){
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function showReportEmpty(){
  reportEmptyState.classList.remove("hidden");
  reportLoading.classList.add("hidden");
  reportContent.classList.add("hidden");
}

function showReportLoading(){
  reportEmptyState.classList.add("hidden");
  reportLoading.classList.remove("hidden");
  reportContent.classList.add("hidden");
}

function showReportContent(){
  reportEmptyState.classList.add("hidden");
  reportLoading.classList.add("hidden");
  reportContent.classList.remove("hidden");
}

async function generateReport(patientId){
  showReportLoading();

  try {
    const report = await apiPost("/generate_report", { patient_id: patientId });

    if(report.error){
      reportLoading.classList.add("hidden");
      reportEmptyState.classList.remove("hidden");
      reportEmptyState.innerHTML = `
        <div class="report-empty-icon">⚠️</div>
        <h2>Cannot Generate Report</h2>
        <p>${escapeHtml(report.error)}</p>
      `;
      return;
    }

    renderReport(report);
    showReportContent();

  } catch(err){
    console.error("Report generation error:", err);
    reportLoading.classList.add("hidden");
    reportEmptyState.classList.remove("hidden");
    reportEmptyState.innerHTML = `
      <div class="report-empty-icon">❌</div>
      <h2>Error</h2>
      <p>Failed to generate report. Please try again.</p>
    `;
  }
}

function renderReport(report){

  // Header
  reportHeaderCard.innerHTML = `
    <div class="report-title-row">
      <h2>📋 Report: ${escapeHtml(report.patient_name)}</h2>
      <span class="report-timestamp">Generated: ${escapeHtml(report.generated_at)}</span>
    </div>
  `;

  // Stats cards
  reportStats.innerHTML = `
    <div class="stat-card">
      <div class="stat-value">${report.total_sessions}</div>
      <div class="stat-label">Total Sessions</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${report.total_messages}</div>
      <div class="stat-label">Total Messages</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${report.sessions.length > 0 ? Math.round(report.total_messages / report.total_sessions) : 0}</div>
      <div class="stat-label">Avg Msgs/Session</div>
    </div>
  `;

  // Session breakdown
  let sessionsHtml = `<h3 class="report-section-title">📁 Session Breakdown</h3><div class="session-cards">`;
  report.sessions.forEach((s, idx) => {
    sessionsHtml += `
      <div class="report-session-card">
        <div class="report-session-name">${escapeHtml(s.name)}</div>
        <div class="report-session-detail">
          <span>📅 ${escapeHtml(s.created_at)}</span>
          <span>💬 ${s.message_count} messages</span>
        </div>
      </div>
    `;
  });
  sessionsHtml += `</div>`;
  reportSessionsGrid.innerHTML = sessionsHtml;

  // AI Analysis — render markdown-like formatting
  const formattedAnalysis = formatAnalysisText(report.ai_analysis);
  reportAiAnalysis.innerHTML = `
    <h3 class="report-section-title">🧠 AI Analysis</h3>
    <div class="analysis-content">${formattedAnalysis}</div>
  `;

  // Footer
  reportFooter.innerHTML = `
    <p>Report generated by Electron Care AI — ${escapeHtml(report.generated_at)}</p>
    <button class="card-btn report-print-btn" onclick="printReport()">🖨️ Print Report</button>
  `;
}

function formatAnalysisText(text){
  if(!text) return "<p>No analysis available.</p>";

  // Escape HTML first
  let escaped = escapeHtml(text);

  // Bold: **text**
  escaped = escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Headers: lines starting with number followed by period
  escaped = escaped.replace(/^(\d+\.\s*)(<strong>.*?<\/strong>)/gm, '<h4 class="analysis-heading">$1$2</h4>');

  // Bullet points
  escaped = escaped.replace(/^[\-\*]\s+(.+)$/gm, '<li>$1</li>');
  escaped = escaped.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
  // Clean double-wrapped uls
  escaped = escaped.replace(/<\/ul>\s*<ul>/g, '');

  // Paragraphs for remaining lines
  escaped = escaped.replace(/\n\n/g, '</p><p>');
  escaped = escaped.replace(/\n/g, '<br>');

  return `<p>${escaped}</p>`;
}

function printReport(){
  const content = reportContent.innerHTML;
  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <html>
    <head>
      <title>Electron Care - Patient Report</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 40px; color: #1a1a1a; }
        h2 { color: #0a1324; margin-bottom: 8px; }
        h3 { color: #16233a; margin: 24px 0 12px; }
        h4 { color: #22314d; margin: 16px 0 8px; }
        .stat-card { display: inline-block; padding: 16px 24px; margin: 8px; border: 1px solid #ddd; border-radius: 12px; text-align: center; }
        .stat-value { font-size: 28px; font-weight: 700; color: #0a1324; }
        .stat-label { font-size: 13px; color: #666; margin-top: 4px; }
        .report-session-card { padding: 12px; border: 1px solid #ddd; border-radius: 10px; margin: 8px 0; }
        .report-session-name { font-weight: 600; }
        .report-session-detail { color: #666; font-size: 13px; margin-top: 4px; }
        .report-session-detail span { margin-right: 16px; }
        .analysis-content { line-height: 1.8; }
        .report-print-btn { display: none; }
        .report-timestamp { color: #666; font-size: 14px; }
        ul { padding-left: 20px; }
        li { margin: 4px 0; }
        strong { color: #0a1324; }
      </style>
    </head>
    <body>${content}</body>
    </html>
  `);
  printWindow.document.close();
  printWindow.print();
}