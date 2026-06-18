from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import UserProgress, QuizResult, Profile

overview_bp = Blueprint('overview_bp', __name__)

@overview_bp.route('/api/overview', methods=['GET'])
@login_required
def get_overview():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    completed_count = UserProgress.query.filter_by(user_id=current_user.id, completed=True).count()
    total_tasks = 17
    progress_pct = round((completed_count / total_tasks) * 100) if total_tasks else 0
    latest_quiz = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.taken_at.desc()).first()

    compatibility_scores = {}
    if latest_quiz and latest_quiz.compatibility_scores:
        try:
            import json
            compatibility_scores = json.loads(latest_quiz.compatibility_scores)
        except Exception:
            compatibility_scores = {}

    return jsonify({
        'career_goal': profile.career_goal if profile else 'Not Set',
        'progress_pct': progress_pct,
        'tasks_done': f"{completed_count} / {total_tasks}",
        'quiz_score': f"{latest_quiz.percentage}%" if latest_quiz else 'No quiz taken',
        'latest_quiz_date': latest_quiz.taken_at.strftime('%Y-%m-%d') if latest_quiz else None,
        'compatibility_scores': compatibility_scores
    }), 200
