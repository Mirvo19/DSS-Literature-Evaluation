from flask import Blueprint, render_template
from utils.auth import require_admin, is_current_request_admin

# english page routes

bp = Blueprint('en_pages', __name__, url_prefix='/en')

LANG = 'en'

# auth pages

@bp.route('/login')
def login_page():
    return render_template('en/login.html', lang=LANG)

@bp.route('/signup')
def signup_page():
    return render_template('en/signup.html', lang=LANG)

# main pages

@bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html', lang=LANG, is_admin=is_current_request_admin())

@bp.route('/winners')
def winners_page():
    return render_template('winners.html', lang=LANG, is_admin=is_current_request_admin())

@bp.route('/week/<week_id>')
def week_detail_page(week_id):
    return render_template('week-detail.html', lang=LANG, is_admin=is_current_request_admin())

@bp.route('/week-rankings/<week_id>')
def week_rankings_page(week_id):
    return render_template('week-rankings.html', lang=LANG)

# admin pages

@bp.route('/admin/dashboard')
@require_admin
def admin_dashboard_page():
    return render_template('admin/dashboard.html', lang=LANG)

@bp.route('/admin/students')
@require_admin
def admin_students_page():
    return render_template('admin/students.html', lang=LANG)

@bp.route('/admin/sessions')
@require_admin
def admin_sessions_page():
    return render_template('admin/sessions.html', lang=LANG)

@bp.route('/admin/weeks')
@require_admin
def admin_weeks_page():
    return render_template('admin/weeks.html', lang=LANG)

@bp.route('/admin/logs')
@require_admin
def admin_logs_page():
    return render_template('admin/logs.html', lang=LANG)

@bp.route('/admin/judge-permissions')
@require_admin
def admin_judge_permissions_page():
    return render_template('admin/judge_permissions.html', lang=LANG)

@bp.route('/admin/results')
@require_admin
def admin_results_page():
    return render_template('admin/results.html', lang=LANG)

@bp.route('/admin/qa-accounts')
@require_admin
def admin_qa_accounts_page():
    return render_template('admin/qa_accounts.html', lang=LANG)

# judge pages

@bp.route('/judge/scoring')
def judge_scoring_page():
    return render_template('judge/scoring.html', lang=LANG)

