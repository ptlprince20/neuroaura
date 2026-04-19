<div align="center">

<img src="https://img.shields.io/badge/Neuro--Aura-Learning%20OS-blueviolet?style=for-the-badge&logo=brain&logoColor=white" alt="Neuro-Aura Badge"/>

# 🧠 Neuro-Aura: Total Mastery Learning OS

**A high-fidelity, AI-augmented Learning Operating System built for Computer Science students who refuse to settle for average.**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/ptlprince20/neuroaura?style=flat-square&color=gold)](https://github.com/ptlprince20/neuroaura/stargazers)

---

> *"Not just an app. A Cognitive Operating System for the Next-Gen CS Student."*

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ptlprince20/neuroaura)

</div>

---

## 📸 Preview

| Dashboard | Topic Quiz Engine | Login Gateway |
|:---:|:---:|:---:|
| Midnight Obsidian dark UI | 4-Subject, 15-Q Quiz System | Google + Guest Auth |

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🧬 **Cognitive DNA Suite** | Tracks Learning Style, Processing Speed, Working Memory & Cognitive Load in real time |
| 🏆 **Mastery Engine** | Weekly Streak Tracker that increments with every active learning session |
| 📚 **Topic Quiz System** | 60 curated questions across 4 subjects — 15 per topic, subject-strict delivery |
| 🎬 **Video Sessions** | Embedded YouTube sessions for OS, DBMS, DSA, Python |
| 🤖 **Aura Assistant** | Floating AI chatbot with contextual learning help |
| 📄 **PDF Report Export** | Export your full mastery dashboard as a professional PDF |
| 🌓 **Dynamic Theming** | Light/Dark mode toggle with `localStorage` persistence |
| 🔐 **Auth Gateway** | Google Sign-In (OAuth 2.0) + instant Guest Mode bypass |
| 🚀 **Vercel Serverless** | Fully serverless-compatible with dynamic `/tmp` SQLite path |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      BROWSER (Client)                       │
│  login.html  ←──→  dashboard.html  ←──→  engine.js (SPA)   │
│  Google GIS SDK     html2pdf.js          Aura Chatbot       │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP / REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (app.py)                    │
│                                                             │
│   /           → Dashboard Route (Auth Guard)                │
│   /login       → Session Auth + Password Hash               │
│   /auth/google → Google OAuth Token Verification            │
│   /api/quiz    → Subject-Strict Quiz Engine (15 Qs)         │
│   /api/submit  → XP, Level, Cognitive Load Calculator       │
│   /api/set_goal→ Daily Goal Synchronization                 │
└───────────────────────────┬─────────────────────────────────┘
                            │ SQLAlchemy ORM
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite DATABASE                           │
│                                                             │
│   User      → id, username, level, xp, cognitive metrics   │
│   Subject   → OS, DBMS, DSA, Python + mastery %            │
│   Question  → 60 questions (15/subject) with answers        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
NEURO-Aura/
│
├── app.py                  # Core Flask backend, REST APIs, DB init & seeding
├── requirements.txt        # Python dependencies (Flask, SQLAlchemy, Gunicorn)
├── render.yaml             # Render.com deployment blueprint
├── vercel.json             # Vercel serverless deployment config
├── drop_db.py              # Utility: wipe and re-seed the database
│
├── templates/
│   ├── dashboard.html      # Main OS dashboard (SPA-style UI)
│   ├── login.html          # Premium auth gateway (Google + Guest)
│   └── register.html       # User registration page
│
├── static/
│   ├── css/
│   │   └── theme.css       # Full design system (dark + light theme tokens)
│   └── js/
│       └── engine.js       # Master JS engine: quiz, video, chatbot, theming
│
└── instance/
    └── neuroaura_total.db  # SQLite database (auto-created on first run)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.14, Flask 3.x |
| **Database** | SQLite via Flask-SQLAlchemy ORM |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JavaScript ES6+ |
| **Authentication** | Google Identity Services (GIS) OAuth 2.0 + Session-based |
| **PDF Export** | `html2pdf.js` CDN |
| **Fonts** | Google Fonts — Plus Jakarta Sans |
| **Deployment** | Vercel (Serverless) / Render.com / PythonAnywhere |
| **Production Server** | Gunicorn WSGI |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+ installed
- `pip` package manager

### 1. Clone the Repository
```bash
git clone https://github.com/ptlprince20/neuroaura.git
cd neuroaura/NEURO-Aura
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
```
http://127.0.0.1:6060
```

> **Default Credentials**: Username: `demo` | Password: `demo123`  
> Or click **"Proceed as Guest"** on the login page for instant access.

---

## 🔄 Database Reset (if needed)

If subjects or questions are missing, run:
```bash
python drop_db.py
python app.py
```
This wipes the database and re-seeds all 60 questions across 4 subjects.

---

## 🧪 Testing the Features

| Feature | How to Test |
|---|---|
| **Login** | Click "Proceed as Guest" — instant dashboard access |
| **Topic Quiz** | Dashboard → Action Hub → "Topic Quiz" → Pick subject → 15 questions delivered |
| **Challenge Mode** | Action Hub → "Challenge Mode" → Select difficulty |
| **Video Session** | Learning Path → Click "▶ Video" on any subject node |
| **Streak Tracker** | Complete any quiz or video — watch the 🔥 counter update live |
| **Goal Setting** | Sidebar goal input → Enter a number → Click Set Goal |
| **PDF Export** | Action Hub → "Export Report" → Downloads full dashboard as PDF |
| **Theme Toggle** | Top-right toggle → Switch between Dark and Light mode |
| **Aura Assistant** | Bottom-right 🤖 button → Chat with the AI learning assistant |

---

## 📊 Quiz System Details

**60 curated questions** across 4 Computer Science subjects:

| Subject | Questions | Topics Covered |
|---|---|---|
| 📀 **Operating Systems** | 15 | Scheduling, Deadlocks, Paging, Virtual Memory, Semaphores, Banker's Algo |
| 🗄️ **DBMS Fundamentals** | 15 | Normalization, ACID, SQL Joins, Indexing, Transactions, NoSQL |
| ⚡ **Data Structures & Algorithms** | 15 | Sorting, Trees, Graphs, Dijkstra, Hash Tables, Complexity |
| 🐍 **Python Programming** | 15 | OOP, Lambda, List Comprehension, Decorators, Built-ins |

---

## 🌐 Deployment

### Deploy to Vercel (Recommended — Free, No Card)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ptlprince20/neuroaura)

1. Click the button above
2. Sign in with GitHub
3. Click **Deploy** — live in 60 seconds!

### Manual Vercel Deployment
```bash
npm install -g vercel
vercel --prod
```

---

## 🛣️ Roadmap

- [x] Core Dashboard with Cognitive DNA metrics  
- [x] 60-question Quiz Engine (15 per subject, subject-strict)  
- [x] Video Sessions with YouTube embed  
- [x] Aura AI Chatbot  
- [x] PDF Report Export  
- [x] Light/Dark Theme Engine  
- [x] Google OAuth 2.0 Integration  
- [x] Vercel Serverless Deployment  
- [ ] Real-time Multiplayer Study Mode  
- [ ] LLM-powered Aura Bot (OpenAI / Gemini)  
- [ ] PostgreSQL migration for persistent production data  
- [ ] Mobile-responsive design overhaul  

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---


---

<div align="center">

**Built with 🧠 and ☕ — Neuro-Aura OS © 2026**

*"Master the system. Master yourself."*

</div>
