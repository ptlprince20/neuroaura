/**
 * Neuro-aura Mastery Engine v4.0 - Hardened Global Interactivity
 */

let currentQuiz = null;
let quizIndex = 0;
let score = 0;
let uiStreakScore = 0;

// Explicit Global Binds
window.openQuiz = openQuiz;
window.submitAnswer = submitAnswer;
window.closeModal = closeModal;
window.setGoal = setGoal;
window.exportReport = exportReport;
window.filterRoadmap = filterRoadmap;
window.openVideo = openVideo;
window.toggleChatBot = toggleChatBot;
window.closeChatBot = closeChatBot;
window.openQuizReview = openQuizReview;
window.openVideoReview = openVideoReview;
window.toggleTheme = toggleTheme;
window.handleChat = handleChat;

/**
 * Streak & Feedback System
 */
function addStreakPoint() {
    uiStreakScore++;
    const streakElem = document.getElementById('sidebar-streak');
    if (streakElem) {
        streakElem.innerText = `${uiStreakScore} 🔥`;
        streakElem.style.transform = 'scale(1.2)';
        setTimeout(() => streakElem.style.transform = 'scale(1)', 300);
    }
}

function showAlert(msg) {
    const toast = document.getElementById('aura-toast');
    const msgElem = document.getElementById('alert-msg');
    if (!toast || !msgElem) return;
    msgElem.innerText = msg;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 5000);
}

/**
 * Quiz & Topic Engine
 */
async function openQuiz(subject) {
    const modal = document.getElementById('master-modal');
    const body = document.getElementById('modal-body');
    if (!modal || !body) return;

    modal.classList.remove('hidden');

    let displaySubject = subject;
    let apiQuery = subject;

    if (subject === 'Challenge') {
        const diff = prompt("Select Mode Difficulty:\n(Easy, Intermediate, Hard)", "Hard");
        if (!diff) { modal.classList.add('hidden'); return; }
        displaySubject = `Challenge Mode [${diff.toUpperCase()}]`;
        showAlert(`Initializing ${diff} Neural Protocol...`);

    } else if (subject === 'Interactive') {
        // Show a subject picker inside the modal — clean and professional
        body.innerHTML = `
            <h3 style="color: var(--cobalt); margin-bottom: 10px;">📚 Topic Quiz — Select Subject</h3>
            <p style="color: var(--text-dim); font-size: 0.9rem; margin-bottom: 25px;">Pick a subject to get 15 targeted questions for that topic only.</p>
            <div style="display: grid; gap: 14px;">
                ${[
                    { label: '📀 Operating Systems', key: 'Operating Systems' },
                    { label: '🗄️ DBMS Fundamentals', key: 'DBMS' },
                    { label: '⚡ Data Structures & Algorithms', key: 'Data Structures' },
                    { label: '🐍 Python Programming', key: 'Python' }
                ].map(s => `
                    <button class="glass" style="padding: 16px 20px; text-align: left; color: white; cursor: pointer; font-size: 1rem; font-weight: 600; border-left: 3px solid var(--cobalt); transition: background 0.3s;"
                        onclick="loadTopicQuiz('${s.key}', '${s.label}')">
                        ${s.label}
                    </button>
                `).join('')}
            </div>
        `;
        return; // Don't fetch yet — wait for subject selection

    } else if (subject !== 'Review') {
        displaySubject = subject;
    }

    body.innerHTML = `<h3 style="color: var(--cobalt);">Aura OS: Fetching ${displaySubject} questions...</h3><p style="color: var(--text-dim);">Loading 15 targeted questions...</p>`;

    try {
        const response = await fetch(`/api/quiz/${encodeURIComponent(apiQuery)}`);
        const data = await response.json();

        if (data.error || !data.length) {
            body.innerHTML = `<h3>${subject} Module</h3><p>No questions found. Please check back shortly.</p>`;
            return;
        }

        currentQuiz = data;
        quizIndex = 0;
        score = 0;
        showQuestion();
    } catch (err) {
        console.error("Quiz Sync Error:", err);
        body.innerHTML = "<h3>Sync Error</h3><p>Neural link interrupted. Please check connection.</p>";
    }
}

// Called after user picks a subject in the Interactive picker
async function loadTopicQuiz(subjectKey, subjectLabel) {
    const body = document.getElementById('modal-body');
    body.innerHTML = `<h3 style="color: var(--cobalt);">Loading ${subjectLabel} questions...</h3><p style="color: var(--text-dim);">Fetching 15 subject-specific questions...</p>`;

    try {
        const response = await fetch(`/api/quiz/${encodeURIComponent(subjectKey)}`);
        const data = await response.json();

        if (data.error || !data.length) {
            body.innerHTML = `<h3>${subjectLabel}</h3><p>No questions found for this subject yet.</p>`;
            return;
        }

        currentQuiz = data;
        quizIndex = 0;
        score = 0;
        showAlert(`Launching ${subjectLabel} — ${data.length} questions loaded!`);
        showQuestion();
    } catch (err) {
        body.innerHTML = "<h3>Sync Error</h3><p>Neural link interrupted. Please check connection.</p>";
    }
}
window.loadTopicQuiz = loadTopicQuiz;

function showQuestion() {
    const body = document.getElementById('modal-body');
    const q = currentQuiz[quizIndex];
    if (!q) return;
    
    body.innerHTML = `
        <h4 style="color: var(--cobalt); margin-bottom: 20px;">Analytic Challenge ${quizIndex + 1}/${currentQuiz.length}</h4>
        <p style="font-size: 1.1rem; margin-bottom: 30px;">${q.text}</p>
        <div style="display: grid; gap: 15px;">
            ${Object.entries(q.options).filter(([k,v]) => v).map(([key, val]) => `
                <button class="glass" style="padding: 15px; text-align: left; color: white; cursor: pointer; transition: background 0.3s;" onclick="submitAnswer('${key}', this)">
                    <strong>${key}:</strong> ${val}
                </button>
            `).join('')}
        </div>
    `;
}

async function submitAnswer(ans, btnElement) {
    const q = currentQuiz[quizIndex];
    const allBtns = document.querySelectorAll('#modal-body button.glass');
    
    if (ans === q.correct) {
        btnElement.style.background = 'rgba(16, 185, 129, 0.5)'; // Green
        score++; 
    } else {
        btnElement.style.background = 'rgba(239, 68, 68, 0.5)'; // Red
        allBtns.forEach(b => {
             if (b.innerText.startsWith(q.correct + ":")) {
                 b.style.background = 'rgba(16, 185, 129, 0.5)'; // Green
             }
        });
    }
    
    allBtns.forEach(b => b.style.pointerEvents = 'none');
    quizIndex++;
    
    setTimeout(() => {
        if (quizIndex < currentQuiz.length) {
            showQuestion();
        } else {
            finishQuiz();
        }
    }, 1500);
}

async function finishQuiz() {
    const body = document.getElementById('modal-body');
    body.innerHTML = `<h3>Neural Analysis in Progress...</h3>`;
    
    try {
        const response = await fetch('/api/submit_quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score: score })
        });
        const data = await response.json();
        
        body.innerHTML = `
            <h3 style="color: var(--teal);">Analytic Report Complete</h3>
            <div style="margin-top: 20px;">
                <p>Mastery Gain: +${score * 10} XP</p>
                <p>Cognitive Load: ${data.new_load}/10</p>
                <div class="glass" style="margin-top: 20px; padding: 15px; border-color: var(--cobalt);">
                    <strong style="color: var(--cobalt);">AI Recommendation:</strong><br>
                    ${data.ai_recommendation}
                </div>
            </div>
        `;
        
        addStreakPoint();
        updateOSDashboard(data);
    } catch (err) {
        body.innerHTML = "<h3>Submission Error</h3><p>Report could not be saved to Neural Core.</p>";
    }
}

/**
 * Dashboard & Goals
 */
async function setGoal() {
    const val = document.getElementById('goal-input').value;
    if (!val) return;
    await fetch('/api/set_goal', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ value: val }) });
    showAlert(`Neural Goal Synchronized: Aiming for ${val} XP today.`);
    updateOSDashboard({ new_goal: 0 }); 
}

function updateOSDashboard(data) {
    if (data.new_goal !== undefined) {
        const circle = document.getElementById('gauge-circle');
        const valText = document.getElementById('gauge-val');
        if (circle && valText) {
            const offset = 251.2 * (1 - data.new_goal / 100);
            circle.style.strokeDashoffset = offset;
            valText.textContent = `${data.new_goal}%`;
        }
    }
    const loadVal = document.getElementById('load-val');
    if (data.new_load !== undefined && loadVal) {
        loadVal.innerText = `${data.new_load} / 10`;
    }
}

/**
 * Interface Controls
 */
function closeModal(id) {
    const elem = document.getElementById(id);
    if (!elem) return;
    elem.classList.add('hidden');
    if (id === 'video-modal') {
        document.getElementById('video-iframe').src = "";
    }
}

function filterRoadmap() {
    const input = document.getElementById('master-search').value.toLowerCase();
    const nodes = document.querySelectorAll('.road-node');
    nodes.forEach(node => {
        const textContent = node.innerText.toLowerCase();
        const titleAttr = node.getAttribute('data-title').toLowerCase();
        if (textContent.includes(input) || titleAttr.includes(input)) {
            node.style.display = 'flex';
        } else {
            node.style.display = 'none';
        }
    });
}

function openVideo(subject) {
    const topic = prompt(`Enter specific topic to watch for ${subject}:`, `Basics of ${subject}`);
    if (!topic) return;
    
    document.getElementById('video-title').innerText = `Video Session: ${subject} - ${topic}`;
    
    let vId = 'bJzb-RuUcMU'; // Default
    const s = subject.toLowerCase();
    if (s.includes('python')) vId = '_uQrJ0TkZlc';
    if (s.includes('dbms') || s.includes('database')) vId = 'HXV3zeJZ1EQ';
    if (s.includes('algorithm') || s.includes('dsa')) vId = '8hly31xKli0';
    if (s.includes('operating')) vId = 'vBURTt97EkA';
    
    document.getElementById('video-iframe').src = `https://www.youtube.com/embed/${vId}?autoplay=1`;
    showAlert(`Starting Neural Video Link for: ${topic}`);
    addStreakPoint();
    document.getElementById('video-modal').classList.remove('hidden');
}

/**
 * Action Hub Extras
 */
function openQuizReview() {
    const modal = document.getElementById('master-modal');
    const body = document.getElementById('modal-body');
    if (!modal || !body) return;

    body.innerHTML = `
        <h3 style="color: var(--amethyst); margin-bottom: 20px;">Past Quiz Analysis</h3>
        <div class="glass" style="padding: 15px; border-left: 3px solid var(--teal); margin-bottom: 20px;">
            <strong style="color: white;">Aura Suggestion:</strong> Re-take the 'Process Synchronization' module to stabilize metrics.
        </div>
        <p style="font-size: 0.9rem; color: var(--text-dim);">Recent Neural Gaps:</p>
        <ul style="margin-top: 10px; margin-left: 20px; font-size: 0.9rem; color: white;">
            <li>Operating Systems: Deadlock Conditions</li>
            <li>DSA: Stack vs Queue complexity</li>
        </ul>
    `;
    modal.classList.remove('hidden');
}

function openVideoReview() {
    const modal = document.getElementById('master-modal');
    const body = document.getElementById('modal-body');
    if (!modal || !body) return;

    body.innerHTML = `
        <h3 style="color: var(--teal); margin-bottom: 20px;">Video Watch History</h3>
        <div style="display: grid; gap: 15px;">
            <div class="glass" style="padding: 15px;">
                <strong style="color: white; display: block;">▶ Python Advanced Concepts</strong>
                <p style="color: var(--text-dim); font-size: 0.8rem;">Status: 100% | Neural Match: High</p>
            </div>
            <div class="glass" style="padding: 15px;">
                <strong style="color: white; display: block;">▶ Query Optimization (DBMS)</strong>
                <p style="color: var(--text-dim); font-size: 0.8rem;">Status: 30% | Refocus required</p>
            </div>
        </div>
    `;
    modal.classList.remove('hidden');
}

function exportReport() {
    showAlert("Generating Professional Mastery Report...");
    const element = document.getElementById('export-container');
    if (!element) return;
    
    const opt = {
        margin: 10,
        filename: 'NeuroAura_Mastery_Report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' }
    };
    html2pdf().set(opt).from(element).save();
}

/**
 * ChatBot & Theming
 */
function toggleChatBot() {
    const panel = document.getElementById('chat-panel');
    if (!panel) return;
    panel.style.display = 'flex';
    panel.classList.toggle('hidden');
}

function closeChatBot() {
    const panel = document.getElementById('chat-panel');
    if (!panel) return;
    panel.style.display = 'none';
    panel.classList.add('hidden');
}

function handleChat(e) {
    if (e.key === 'Enter' && e.target.value.trim() !== '') {
        const msgList = document.getElementById('chat-messages');
        const userText = e.target.value;
        msgList.innerHTML += `<div class="chat-msg" style="text-align: right; color: white;">${userText}</div>`;
        e.target.value = '';
        
        setTimeout(() => {
            let reply = "I'm analyzing your path. Check the Action Hub for specific reviews!";
            const lowerText = userText.toLowerCase();
            if (lowerText.includes('quiz')) reply = "To start a quiz, navigate to the Roadmap or click 'Challenge Mode'.";
            if (lowerText.includes('video')) reply = "All subjects have '▶ Video' buttons linked to your neural curriculum.";
            
            msgList.innerHTML += `<div class="chat-msg aura">${reply}</div>`;
            msgList.scrollTop = msgList.scrollHeight;
        }, 800);
    }
}

function toggleTheme() {
    document.body.classList.toggle('light-theme');
    localStorage.setItem('neuro-aura-theme', document.body.classList.contains('light-theme') ? 'light' : 'dark');
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('neuro-aura-theme') === 'light') {
        document.body.classList.add('light-theme');
    }
    console.log("Neuro-aura OS: Neural Core Operational.");
});
