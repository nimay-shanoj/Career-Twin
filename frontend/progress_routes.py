from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import UserProgress
from extensions import db

progress_bp = Blueprint('progress_bp', __name__)

PROGRESS_TASKS = [
    {"id": 1, "goal": "Python Developer", "task": "Python Basics", "desc": "Variables, loops, conditionals"},
    {"id": 2, "goal": "Python Developer", "task": "OOP in Python", "desc": "Classes, inheritance, methods"},
    {"id": 3, "goal": "Python Developer", "task": "File Handling", "desc": "Read/write files with Python"},
    {"id": 4, "goal": "Python Developer", "task": "MySQL with Python", "desc": "Connect and query a database"},
    {"id": 5, "goal": "Python Developer", "task": "Flask Basics", "desc": "Build a simple web app"},
    {"id": 6, "goal": "Backend Developer", "task": "REST API Design", "desc": "Understand HTTP methods & endpoints"},
    {"id": 7, "goal": "Backend Developer", "task": "Django Setup", "desc": "Create a Django project"},
    {"id": 8, "goal": "Backend Developer", "task": "Authentication", "desc": "User login & JWT tokens"},
    {"id": 9, "goal": "Backend Developer", "task": "Database Modeling", "desc": "Design tables and relationships"},
    {"id": 10, "goal": "Full Stack Developer", "task": "HTML & CSS", "desc": "Build responsive web pages"},
    {"id": 11, "goal": "Full Stack Developer", "task": "JavaScript Basics", "desc": "DOM, events, fetch API"},
    {"id": 12, "goal": "Full Stack Developer", "task": "React Fundamentals", "desc": "Components, props, state"},
    {"id": 13, "goal": "Full Stack Developer", "task": "Django + React", "desc": "Connect frontend and backend"},
    {"id": 14, "goal": "Data Analyst", "task": "Python for Data", "desc": "NumPy and Pandas basics"},
    {"id": 15, "goal": "Data Analyst", "task": "SQL Querying", "desc": "SELECT, JOIN, GROUP BY"},
    {"id": 16, "goal": "Data Analyst", "task": "Data Visualization", "desc": "Matplotlib and Seaborn"},
    {"id": 17, "goal": "Data Analyst", "task": "Power BI", "desc": "Build an interactive dashboard"}
]

@progress_bp.route('/api/progress', methods=['GET'])
@login_required
def get_progress():
    completed = UserProgress.query.filter_by(user_id=current_user.id, completed=True).all()
    completed_ids = [item.task_id for item in completed]
    total = len(PROGRESS_TASKS)
    completed_count = len(completed_ids)
    progress_pct = round((completed_count / total) * 100) if total else 0

    tasks_response = []
    for task in PROGRESS_TASKS:
        tasks_response.append({
            'id': task['id'],
            'goal': task['goal'],
            'task': task['task'],
            'desc': task['desc'],
            'completed': task['id'] in completed_ids
        })

    return jsonify({
        'tasks': tasks_response,
        'completed_ids': completed_ids,
        'completed_count': completed_count,
        'total_tasks': total,
        'progress_pct': progress_pct
    }), 200

@progress_bp.route('/api/progress/toggle', methods=['POST'])
@login_required
def toggle_progress():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request payload'}), 400

    task_id = data.get('task_id')
    completed = data.get('completed')

    if task_id is None or completed is None:
        return jsonify({'error': 'task_id and completed are required'}), 400

    record = UserProgress.query.filter_by(user_id=current_user.id, task_id=task_id).first()
    if not record:
        record = UserProgress(user_id=current_user.id, task_id=task_id, completed=bool(completed))
        db.session.add(record)
    else:
        record.completed = bool(completed)

    try:
        db.session.commit()
        return jsonify({'success': True, 'task_id': task_id, 'completed': bool(completed)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Could not update progress task'}), 500

@progress_bp.route('/api/progress/reset', methods=['POST'])
@login_required
def reset_progress():
    try:
        UserProgress.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Could not reset progress'}), 500
