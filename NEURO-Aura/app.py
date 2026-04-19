import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
import json
import random
import requests as http_requests

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
    option_a = db.Column(db.String(200))
    option_b = db.Column(db.String(200))
    option_c = db.Column(db.String(200))
    option_d = db.Column(db.String(200))
    correct = db.Column(db.String(1))

# --- Serverless Initialization ---

def init_db():
    with app.app_context():
        db.create_all()
        # Force re-seed if questions are missing or incomplete (fixes Vercel stale DB)
        if Question.query.count() < 60:
            # Wipe old incomplete data
            Question.query.delete()
            Subject.query.delete()
            User.query.delete()
            db.session.commit()

            os_subj   = Subject(title="Operating Systems", category="Core System", icon="📀", mastery=75)
            dbms_subj = Subject(title="DBMS Fundamentals", category="Data Architecture", icon="🗄️", mastery=62)
            dsa_subj  = Subject(title="Data Structures & Algorithms", category="Computational Logic", icon="⚡", mastery=48)
            py_subj   = Subject(title="Python Programming", category="Programming", icon="🐍", mastery=85)
            db.session.add_all([os_subj, dbms_subj, dsa_subj, py_subj])
            db.session.commit()

            # ---- Operating Systems (15 questions) ----
            db.session.add_all([
                Question(subject_id=os_subj.id, text="Which scheduling algorithm is non-preemptive?",
                         option_a="FCFS", option_b="Round Robin", option_c="Shortest Remaining Time", option_d="Multilevel Queue", correct="A"),
                Question(subject_id=os_subj.id, text="What is a 'deadlock'?",
                         option_a="Total system crash", option_b="Infinite loop in user program", option_c="Circular wait for shared resources", option_d="Memory leak", correct="C"),
                Question(subject_id=os_subj.id, text="Which condition is NOT required for deadlock?",
                         option_a="Mutual Exclusion", option_b="Hold and Wait", option_c="Preemption", option_d="Circular Wait", correct="C"),
                Question(subject_id=os_subj.id, text="What does a page fault indicate?",
                         option_a="Hardware failure", option_b="Requested page not in RAM", option_c="Corrupt file system", option_d="Invalid memory address", correct="B"),
                Question(subject_id=os_subj.id, text="Which page replacement algorithm gives minimum page faults (with full knowledge)?",
                         option_a="LRU", option_b="FIFO", option_c="Optimal", option_d="Clock", correct="C"),
                Question(subject_id=os_subj.id, text="What is thrashing in OS?",
                         option_a="CPU spending more time swapping than executing", option_b="Disk failure", option_c="Too many threads", option_d="RAM overflow", correct="A"),
                Question(subject_id=os_subj.id, text="Which is used for inter-process communication?",
                         option_a="Semaphore only", option_b="Pipes, Sockets, Shared Memory", option_c="Registers", option_d="Cache", correct="B"),
                Question(subject_id=os_subj.id, text="A semaphore with value 1 is called?",
                         option_a="Counting semaphore", option_b="Binary semaphore (Mutex)", option_c="Monitor", option_d="Spinlock", correct="B"),
                Question(subject_id=os_subj.id, text="Which OS concept prevents multiple processes from entering critical section simultaneously?",
                         option_a="Paging", option_b="Scheduling", option_c="Mutual Exclusion (Mutex)", option_d="Fragmentation", correct="C"),
                Question(subject_id=os_subj.id, text="What is the role of the OS kernel?",
                         option_a="Manage hardware resources and provide services", option_b="Compile user programs", option_c="Manage network only", option_d="Display UI", correct="A"),
                Question(subject_id=os_subj.id, text="Virtual memory allows programs to use address space that is?",
                         option_a="Exactly equal to RAM", option_b="Smaller than RAM", option_c="Larger than physical RAM", option_d="Same as cache", correct="C"),
                Question(subject_id=os_subj.id, text="In Round Robin scheduling, the time slice given to each process is called?",
                         option_a="Burst time", option_b="Quantum", option_c="Priority", option_d="Epoch", correct="B"),
                Question(subject_id=os_subj.id, text="Which of the following is a preemptive scheduling algorithm?",
                         option_a="FCFS", option_b="SJF (non-preemptive)", option_c="SRJF (Shortest Remaining Job First)", option_d="Priority (non-preemptive)", correct="C"),
                Question(subject_id=os_subj.id, text="Banker's Algorithm is used to?",
                         option_a="Detect deadlock", option_b="Avoid deadlock", option_c="Prevent deadlock by denial of resources", option_d="Recover from deadlock", correct="B"),
                Question(subject_id=os_subj.id, text="What is internal fragmentation?",
                         option_a="Wasted space outside allocated block", option_b="Wasted space inside allocated block", option_c="Fragmented disk sectors", option_d="Memory leaks", correct="B"),
            ])

            # ---- DBMS Fundamentals (15 questions) ----
            db.session.add_all([
                Question(subject_id=dbms_subj.id, text="Which SQL command removes an entire table and its structure?",
                         option_a="DELETE", option_b="DROP", option_c="TRUNCATE", option_d="REMOVE", correct="B"),
                Question(subject_id=dbms_subj.id, text="What does ACID stand for?",
                         option_a="Atomicity, Consistency, Isolation, Durability", option_b="Access, Control, Integrated, Data", option_c="Always, Correct, Indexed, Data", option_d="Atomic, Concurrent, Instance, Delta", correct="A"),
                Question(subject_id=dbms_subj.id, text="Which normal form eliminates transitive dependencies?",
                         option_a="1NF", option_b="2NF", option_c="3NF", option_d="BCNF", correct="C"),
                Question(subject_id=dbms_subj.id, text="What is the purpose of an index in a database?",
                         option_a="Store data permanently", option_b="Speeds up data retrieval", option_c="Create foreign keys", option_d="Encrypt data", correct="B"),
                Question(subject_id=dbms_subj.id, text="Which JOIN returns rows only when there is a match in both tables?",
                         option_a="LEFT JOIN", option_b="RIGHT JOIN", option_c="FULL OUTER JOIN", option_d="INNER JOIN", correct="D"),
                Question(subject_id=dbms_subj.id, text="What is a primary key?",
                         option_a="Uniquely identifies each row in a table", option_b="Can have NULL values", option_c="Is optional in every table", option_d="Links two databases", correct="A"),
                Question(subject_id=dbms_subj.id, text="Which command saves a transaction permanently?",
                         option_a="ROLLBACK", option_b="SAVEPOINT", option_c="COMMIT", option_d="BEGIN", correct="C"),
                Question(subject_id=dbms_subj.id, text="What is denormalization?",
                         option_a="Adding redundancy to improve read performance", option_b="Removing duplicate data", option_c="Splitting tables", option_d="Encrypting a table", correct="A"),
                Question(subject_id=dbms_subj.id, text="Which SQL clause filters groups after GROUP BY?",
                         option_a="WHERE", option_b="HAVING", option_c="FILTER", option_d="ORDER BY", correct="B"),
                Question(subject_id=dbms_subj.id, text="A foreign key in table B refers to the ___ of table A:",
                         option_a="Foreign key", option_b="Primary key", option_c="Any column", option_d="Index column", correct="B"),
                Question(subject_id=dbms_subj.id, text="Which isolation level prevents dirty reads?",
                         option_a="Read Uncommitted", option_b="Read Committed", option_c="Repeatable Read", option_d="Serializable", correct="B"),
                Question(subject_id=dbms_subj.id, text="What does ER stand for in ER Diagram?",
                         option_a="Entity Relationship", option_b="Entity Record", option_c="Entry Row", option_d="Extended Record", correct="A"),
                Question(subject_id=dbms_subj.id, text="Which of these is a NoSQL database?",
                         option_a="MySQL", option_b="PostgreSQL", option_c="MongoDB", option_d="SQLite", correct="C"),
                Question(subject_id=dbms_subj.id, text="What is a view in SQL?",
                         option_a="A physical copy of a table", option_b="A virtual table based on a query", option_c="A stored procedure", option_d="An index structure", correct="B"),
                Question(subject_id=dbms_subj.id, text="Which SQL operation combines rows from two queries?",
                         option_a="JOIN", option_b="UNION", option_c="INTERSECT", option_d="MERGE", correct="B"),
            ])

            # ---- DSA (15 questions) ----
            db.session.add_all([
                Question(subject_id=dsa_subj.id, text="Which data structure uses LIFO order?",
                         option_a="Queue", option_b="Stack", option_c="Linked List", option_d="Heap", correct="B"),
                Question(subject_id=dsa_subj.id, text="Time complexity of Binary Search is?",
                         option_a="O(n)", option_b="O(n²)", option_c="O(log n)", option_d="O(1)", correct="C"),
                Question(subject_id=dsa_subj.id, text="Which sorting algorithm has the best average-case complexity?",
                         option_a="Bubble Sort", option_b="Insertion Sort", option_c="Quick Sort", option_d="Selection Sort", correct="C"),
                Question(subject_id=dsa_subj.id, text="What is the worst-case time complexity of Quick Sort?",
                         option_a="O(n log n)", option_b="O(n²)", option_c="O(n)", option_d="O(log n)", correct="B"),
                Question(subject_id=dsa_subj.id, text="A complete binary tree with n nodes has height?",
                         option_a="n", option_b="log₂(n)", option_c="n/2", option_d="2n", correct="B"),
                Question(subject_id=dsa_subj.id, text="Which traversal visits root first, then left then right?",
                         option_a="Inorder", option_b="Postorder", option_c="Preorder", option_d="Level-order", correct="C"),
                Question(subject_id=dsa_subj.id, text="Dijkstra's algorithm solves?",
                         option_a="Minimum spanning tree", option_b="Single source shortest path", option_c="All pairs shortest path", option_d="Topological sort", correct="B"),
                Question(subject_id=dsa_subj.id, text="A queue uses which order?",
                         option_a="LIFO", option_b="FIFO", option_c="Random", option_d="Priority based", correct="B"),
                Question(subject_id=dsa_subj.id, text="Which data structure is best for implementing a priority queue?",
                         option_a="Stack", option_b="Array", option_c="Heap", option_d="Linked List", correct="C"),
                Question(subject_id=dsa_subj.id, text="What does DFS stand for?",
                         option_a="Data First Search", option_b="Depth First Search", option_c="Dynamic Flow Sort", option_d="Direct Function Stack", correct="B"),
                Question(subject_id=dsa_subj.id, text="A hash table provides average-case lookup in?",
                         option_a="O(n)", option_b="O(log n)", option_c="O(1)", option_d="O(n log n)", correct="C"),
                Question(subject_id=dsa_subj.id, text="Merge Sort is a classic example of?",
                         option_a="Greedy algorithm", option_b="Dynamic programming", option_c="Divide and conquer", option_d="Backtracking", correct="C"),
                Question(subject_id=dsa_subj.id, text="Which operation removes from the front of a queue?",
                         option_a="Push", option_b="Pop", option_c="Enqueue", option_d="Dequeue", correct="D"),
                Question(subject_id=dsa_subj.id, text="A linked list uses nodes that contain data and a?",
                         option_a="Index", option_b="Pointer to next node", option_c="Array index", option_d="Stack frame", correct="B"),
                Question(subject_id=dsa_subj.id, text="Which algorithm finds the minimum spanning tree?",
                         option_a="Dijkstra's", option_b="Floyd-Warshall", option_c="Kruskal's", option_d="DFS", correct="C"),
            ])

            # ---- Python Programming (15 questions) ----
            db.session.add_all([
                Question(subject_id=py_subj.id, text="How do you create a dictionary in Python?",
                         option_a="[]", option_b="()", option_c="{}", option_d="<>", correct="C"),
                Question(subject_id=py_subj.id, text="Which keyword is used to define a function in Python?",
                         option_a="function", option_b="def", option_c="func", option_d="define", correct="B"),
                Question(subject_id=py_subj.id, text="What does `len([1, 2, 3])` return?",
                         option_a="2", option_b="3", option_c="4", option_d="1", correct="B"),
                Question(subject_id=py_subj.id, text="Which of these is immutable in Python?",
                         option_a="List", option_b="Dictionary", option_c="Tuple", option_d="Set", correct="C"),
                Question(subject_id=py_subj.id, text="What does `//` operator do in Python?",
                         option_a="Division", option_b="Floor division", option_c="Modulo", option_d="Power", correct="B"),
                Question(subject_id=py_subj.id, text="Which Python keyword handles exceptions?",
                         option_a="catch", option_b="error", option_c="except", option_d="handle", correct="C"),
                Question(subject_id=py_subj.id, text="What is a lambda function in Python?",
                         option_a="A multi-line function", option_b="An anonymous single-expression function", option_c="A class method", option_d="A built-in function", correct="B"),
                Question(subject_id=py_subj.id, text="Which built-in function converts a string to integer?",
                         option_a="str()", option_b="float()", option_c="int()", option_d="num()", correct="C"),
                Question(subject_id=py_subj.id, text="What does `*args` do in a function definition?",
                         option_a="Passes keyword arguments", option_b="Accepts variable number of positional arguments", option_c="Multiplies arguments", option_d="Creates a list", correct="B"),
                Question(subject_id=py_subj.id, text="Which statement is used to exit a loop early?",
                         option_a="exit", option_b="stop", option_c="break", option_d="return", correct="C"),
                Question(subject_id=py_subj.id, text="What is list comprehension in Python?",
                         option_a="Importing a list library", option_b="A concise way to create lists using an expression", option_c="A type of loop", option_d="A sorting function", correct="B"),
                Question(subject_id=py_subj.id, text="What is the output of `type(3.14)` in Python?",
                         option_a="int", option_b="str", option_c="float", option_d="double", correct="C"),
                Question(subject_id=py_subj.id, text="Which method adds an element to the end of a list?",
                         option_a="add()", option_b="insert()", option_c="push()", option_d="append()", correct="D"),
                Question(subject_id=py_subj.id, text="What does `self` refer to in a Python class?",
                         option_a="The class itself", option_b="The current instance of the class", option_c="The parent class", option_d="A global variable", correct="B"),
                Question(subject_id=py_subj.id, text="What does the `zip()` function do?",
                         option_a="Compresses files", option_b="Combines two iterables element-by-element", option_c="Sorts a list", option_d="Creates a dictionary", correct="B"),
            ])

            if not User.query.filter_by(username="demo").first():
                db.session.add(User(username="demo", password=generate_password_hash("demo123")))
            db.session.commit()

# Run initialization exactly once when the app is imported
init_db()

# --- Google OAuth Route ---
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")

@app.route('/auth/google', methods=['POST'])
def google_auth():
    """Verify Google ID token from frontend and log user in."""
    try:
        token = request.json.get('credential')
        if not token:
            return jsonify({"error": "No credential provided"}), 400

        # Verify token with Google's API
        verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        resp = http_requests.get(verify_url, timeout=5)
        info = resp.json()

        if 'error' in info or 'sub' not in info:
            return jsonify({"error": "Invalid Google token"}), 401

        email = info.get('email', '')
        name  = info.get('name', email.split('@')[0])
        # Use Google's unique sub ID as username
        google_user_id = f"google_{info['sub']}"

        # Create user if first time
        user = User.query.filter_by(username=google_user_id).first()
        if not user:
            user = User(username=google_user_id, password=generate_password_hash(info['sub']))
            db.session.add(user)
            db.session.commit()

        session['user_id'] = user.id
        session['user_name'] = name
        return jsonify({"status": "ok", "redirect": "/"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
            session['user_name'] = user.username
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
    # Generic modes pull from all questions
    if subject_name in ["Challenge", "Review", "Interactive"]:
        qs = Question.query.all()
        sample = random.sample(qs, min(len(qs), 15)) if qs else []
    else:
        # Strict subject filter — only return questions for that specific subject
        subj = Subject.query.filter(Subject.title.ilike(f"%{subject_name}%")).first()
        if not subj: return jsonify({"error": "Subject not found"}), 404
        qs = Question.query.filter_by(subject_id=subj.id).all()
        # Return up to 15 questions for topic quizzes
        sample = random.sample(qs, min(len(qs), 15)) if qs else []

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
