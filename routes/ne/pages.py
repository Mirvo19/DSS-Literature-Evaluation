from flask import Blueprint, render_template

# nepali page routes — all under /ne/, lang='ne' injected into every template

bp = Blueprint('ne_pages', __name__, url_prefix='/ne')

LANG = 'ne'

# auth pages

@bp.route('/login')
def login_page():
    return render_template('ne/login.html', lang=LANG)

@bp.route('/signup')
def signup_page():
    return render_template('ne/signup.html', lang=LANG)

# main pages

@bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html', lang=LANG)

@bp.route('/winners')
def winners_page():
    return render_template('winners.html', lang=LANG)

@bp.route('/week/<week_id>')
def week_detail_page(week_id):
    return render_template('week-detail.html', lang=LANG)

@bp.route('/week-rankings/<week_id>')
def week_rankings_page(week_id):
    return render_template('week-rankings.html', lang=LANG)

# admin pages

@bp.route('/admin/dashboard')
def admin_dashboard_page():
    return render_template('admin/dashboard.html', lang=LANG)

@bp.route('/admin/students')
def admin_students_page():
    return render_template('admin/students.html', lang=LANG)

@bp.route('/admin/sessions')
def admin_sessions_page():
    return render_template('admin/sessions.html', lang=LANG)

@bp.route('/admin/weeks')
def admin_weeks_page():
    return render_template('admin/weeks.html', lang=LANG)

@bp.route('/admin/logs')
def admin_logs_page():
    return render_template('admin/logs.html', lang=LANG)

@bp.route('/admin/judge-permissions')
def admin_judge_permissions_page():
    return render_template('admin/judge_permissions.html', lang=LANG)

@bp.route('/admin/results')
def admin_results_page():
    return render_template('admin/results.html', lang=LANG)

# judge pages

@bp.route('/judge/scoring')
def judge_scoring_page():
    return render_template('judge/scoring.html', lang=LANG)
