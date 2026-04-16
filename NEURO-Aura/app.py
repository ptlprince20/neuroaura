import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neuro_total_mastery_881'
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/neuroaura_total.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neuroaura_total.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Total Mastery Models ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    mental_state = db.Column(db.String(50), default="Flow")
    daily_goal_target = db.Column(db.Integer, default=100)
    current_goal_progress = db.Column(db.Integer, default=45)
    streak_history = db.Column(db.String(50), default="1,1,1,0,0,0,0")
    total_streak_count = db.Column(db.Integer, default=3)
    learning_style = db.Column(db.String(50), default="Visual-Spatial")
    processing_speed = db.Column(db.Integer, default=740)
    working_memory = db.Column(db.Integer, default=82)
    cognitive_load_score = db.Column(db.Integer, default=3)
    engagement_level = db.Column(db.Integer, default=92)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(10), nullable=False)
    mastery = db.Column(db.Integer, default=40)
    is_locked = db.Column(db.Boolean, default=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    text = db.Column(db.String(300), nullable=False)
    option_a = db.Column(db.String(100))
    option_b = db.Column(db.String(100))
    option_c = db.Column(db.String(100))
    option_d = db.Column(db.String(100))
    correct = db.Column(db.String(1))

# --- Serverless Initialization ---

def init_db():
    with app.app_context():
        db.create_all()
        if not Subject.query.first():
            os_subj = Subject(title="Operating Systems", category="Core System", icon="📀", mastery=75)
            dbms_subj = Subject(title="DBMS Fundamentals", category="Data Architecture", icon="🗄️", mastery=62)
            dsa_subj = Subject(title="Data Structures & Algorithms", category="Computational Logic", icon="⚡", mastery=48)
            python_subj = Subject(title="Python Programming", category="Programming", icon="🐍", mastery=85)
            db.session.add_all([os_subj, dbms_subj, dsa_subj, python_subj])
            db.session.commit()
            
            # Seed Questions
            db.session.add_all([
                Question(subject_id=os_subj.id, text="Which scheduling algorithm is non-preemptive?", 
                         option_a="FCFS", option_b="Round Robin", option_c="Priority", option_d="Shortest Job First", correct="A"),
                Question(subject_id=os_subj.id, text="What is a 'deadlock'?", 
                         option_a="Total system crash", option_b="Infinite loop", option_c="Circular wait for resources", option_d="Memory leak", correct="C"),
                Question(subject_id=dbms_subj.id, text="Which SQL command is used to remove a table?", 
                         option_a="DELETE", option_b="DROP", option_c="TRUNCATE", option_d="REMOVE", correct="B"),
                Question(subject_id=dbms_subj.id, text="What does ACID stand for?", 
                         option_a="Atomicity, Consistency, Isolation, Durability", option_b="Access, Control, Integrated, Data", option_c="Always, Correct, Indexed, Data", option_d="Atomic, Concurrent, Instance, Delta", correct="A"),
                Question(subject_id=dsa_subj.id, text="Which data structure uses LIFO?", 
                         option_a="Queue", option_b="Stack", option_c="Tree", option_d="Graph", correct="B"),
                Question(subject_id=python_subj.id, text="How do you create a dictionary in Python?", 
                         option_a="[]", option_b="()", option_c="{}", option_d="<>", correct="C")
            ])
            
            if not User.query.filter_by(username="demo").first():
                db.session.add(User(username="demo", password=generate_password_hash("demo123")))
            db.session.commit()

# Run initialization exactly once when the app is imported
init_db()

# --- Total Mastery Routes ---

@app.route('/')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    subjects = Subject.query.order_by(Subject.id.asc()).all()
    streak_list = [int(x) for x in user.streak_history.split(',')]
    return render_template('dashboard.html', user=user, subjects=subjects, streak_list=streak_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        db.session.add(User(username=request.form['username'], password=hashed_pw))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/api/quiz/<subject_name>')
def get_quiz(subject_name):
    # If the request is for a generic mode, pull questions randomly from anywhere
    if subject_name in ["Challenge", "Review", "Interactive"]:
        qs = Question.query.all()
    else:
        subj = Subject.query.filter(Subject.title.ilike(f"%{subject_name}%")).first()
        if not subj: return jsonify({"error": "Subject not found"}), 404
        qs = Question.query.filter_by(subject_id=subj.id).all()
        
    # Return up to 3 questions randomly
    sample = random.sample(qs, min(len(qs), 3)) if qs else []
    if not sample: return jsonify({"error": "No questions available"}), 404
    
    return jsonify([{
        "id": q.id, "text": q.text, 
        "correct": q.correct,
        "options": {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d}
    } for q in sample])

@app.route('/api/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    score = data.get('score', 0)
    user = User.query.get(session['user_id'])
    
    # Analyze and update cognitive state
    user.xp += (score * 10)
    if user.xp >= 100:
        user.level += 1
        user.xp = 0
    
    user.current_goal_progress = min(100, user.current_goal_progress + (score * 5))
    user.processing_speed = min(1000, user.processing_speed + (score * 20))
    user.cognitive_load_score = max(1, 10 - score)
    
    db.session.commit()
    return jsonify({
        "status": "analyzed",
        "new_level": user.level,
        "new_goal": user.current_goal_progress,
        "new_load": user.cognitive_load_score,
        "ai_recommendation": "Maintain consistency in Memory Management modules." if score > 1 else "Increase focus on fundamental pointers and concurrency."
    })

@app.route('/api/set_goal', methods=['POST'])
def set_goal():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    val = request.json.get('value', 0)
    user.daily_goal_target = val
    user.current_goal_progress = 0
    db.session.commit()
    return jsonify({"status": "goal_set"})

if __name__ == '__main__':
    app.run(debug=True, port=6060)
