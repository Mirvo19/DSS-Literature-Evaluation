from flask import Blueprint, request, jsonify, render_template
from supabase import create_client
from config import Config
from functools import wraps

bp = Blueprint('judge', __name__, url_prefix='/judge')

# init supabase with service key
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

def require_judge(f):
    """Decorator to require judge authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get the authorization token
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'No authorization token'}), 401
            
            token = auth_header[7:]
            # Verify the token with Supabase
            user = supabase.auth.get_user(token)
            if not user or not user.user:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Store user info in request context
            request.current_user = user.user
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication failed', 'details': str(e)}), 401
    return decorated_function

def get_judge_email_from_request():
    """Extract judge email from the current request"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            user = supabase.auth.get_user(token)
            if user and user.user:
                return user.user.email, user.user.id
        return None, None
    except Exception as e:
        print(f"Error getting judge email: {e}")
        return None, None

# ============================================
# JUDGE PAGES
# ============================================

@bp.route('/scoring')
def judge_scoring_page():
    """Judge scoring page"""
    return render_template('judge/scoring.html')

# ============================================
# JUDGE API ENDPOINTS
# ============================================

@bp.route('/api/my-assignments', methods=['GET'])
def get_my_assignments():
    """Get all active judge assignments for the current user"""
    try:
        judge_email, judge_id = get_judge_email_from_request()
        print(f"Judge email check: {judge_email}")
        
        if not judge_email:
            print("No judge email found, returning empty assignments")
            return jsonify({'assignments': []}), 200
        
        # Get active permissions with week and session details
        response = supabase.table('judge_permissions')\
            .select('*, weeks(id, week_number, topic, session_id, sessions(events(name)))')\
            .eq('user_email', judge_email)\
            .eq('is_active', True)\
            .execute()
        
        print(f"Found {len(response.data)} active assignments for {judge_email}")
        print(f"Assignments: {response.data}")
        
        return jsonify({'assignments': response.data}), 200
    except Exception as e:
        print(f"Error in get_my_assignments: {e}")
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        if 'relation "judge_permissions" does not exist' in error_msg or 'table' in error_msg.lower():
            return jsonify({'assignments': [], 'message': 'Judging system not yet configured'}), 200
        return jsonify({'error': error_msg}), 500

@bp.route('/api/week/<week_id>/participants', methods=['GET'])
@require_judge
def get_week_participants(week_id):
    """Get all participants for a week that the judge can score"""
    try:
        judge_email, judge_id = get_judge_email_from_request()
        if not judge_email:
            return jsonify({'error': 'Could not identify judge'}), 401
        
        # Verify judge has permission for this week
        permission = supabase.table('judge_permissions')\
            .select('*')\
            .eq('user_email', judge_email)\
            .eq('week_id', week_id)\
            .eq('is_active', True)\
            .execute()
        
        if not permission.data:
            return jsonify({'error': 'No permission to score this week'}), 403
        
        judge_type = permission.data[0]['judge_type']
        
        # Get all participants for this week
        participants_response = supabase.table('participants')\
            .select('*, students(name, roll_number)')\
            .eq('week_id', week_id)\
            .execute()
        
        # Get existing scores by this judge for these participants
        participant_ids = [p['id'] for p in participants_response.data]
        scores_response = supabase.table('judge_scores')\
            .select('*')\
            .eq('judge_email', judge_email)\
            .eq('judge_type', judge_type)\
            .in_('participant_id', participant_ids)\
            .execute()
        
        # Mark participants as scored or pending
        scored_participant_ids = {s['participant_id'] for s in scores_response.data}
        for participant in participants_response.data:
            participant['scored'] = participant['id'] in scored_participant_ids
        
        return jsonify({
            'participants': participants_response.data,
            'judge_type': judge_type
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/criteria', methods=['GET'])
@require_judge
def get_judging_criteria():
    """Get all judging criteria, optionally filtered by judge type"""
    try:
        judge_type = request.args.get('judge_type')
        
        query = supabase.table('judging_criteria').select('*')
        
        if judge_type:
            query = query.eq('judge_type', judge_type)
        
        response = query.order('id').execute()
        
        return jsonify({'criteria': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/submit-score', methods=['POST'])
@require_judge
def submit_score():
    """Submit or update a score for a participant"""
    try:
        data = request.json
        judge_email, judge_id = get_judge_email_from_request()
        
        if not judge_email:
            return jsonify({'error': 'Could not identify judge'}), 401
        
        if not data.get('participant_id') or not data.get('judge_type'):
            return jsonify({'error': 'Participant ID and judge type are required'}), 400
        
        # Verify judge has permission for this participant's week
        participant = supabase.table('participants')\
            .select('week_id')\
            .eq('id', data['participant_id'])\
            .single()\
            .execute()
        
        if not participant.data:
            return jsonify({'error': 'Participant not found'}), 404
        
        permission = supabase.table('judge_permissions')\
            .select('*')\
            .eq('user_email', judge_email)\
            .eq('week_id', participant.data['week_id'])\
            .eq('judge_type', data['judge_type'])\
            .eq('is_active', True)\
            .execute()
        
        if not permission.data:
            return jsonify({'error': 'No permission to score this participant'}), 403
        
        # Check if score already exists
        existing_score = supabase.table('judge_scores')\
            .select('*')\
            .eq('participant_id', data['participant_id'])\
            .eq('judge_email', judge_email)\
            .eq('judge_type', data['judge_type'])\
            .execute()
        
        score_data = {
            'participant_id': data['participant_id'],
            'judge_email': judge_email,
            'judge_type': data['judge_type'],
            'score': data.get('score', 0),
            'max_score': data.get('max_score', 100),
            'comments': data.get('comments', ''),
            'criteria_breakdown': data.get('criteria_breakdown', {})
        }
        
        if existing_score.data:
            # Update existing score
            response = supabase.table('judge_scores')\
                .update(score_data)\
                .eq('id', existing_score.data[0]['id'])\
                .execute()
        else:
            # Insert new score
            response = supabase.table('judge_scores')\
                .insert(score_data)\
                .execute()
        
        return jsonify({
            'message': 'Score submitted successfully',
            'score': response.data[0]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/my-scores', methods=['GET'])
def get_my_scores():
    """Get all scores submitted by the current judge"""
    try:
        judge_email, judge_id = get_judge_email_from_request()
        if not judge_email:
            return jsonify({'scores': []}), 200
        
        response = supabase.table('judge_scores')\
            .select('*')\
            .eq('judge_email', judge_email)\
            .execute()
        
        print(f"Found {len(response.data)} scores for judge {judge_email}")
        
        # Enrich scores with participant and student data
        for score in response.data:
            try:
                participant = supabase.table('participants')\
                    .select('id, student_id, week_id')\
                    .eq('id', score['participant_id'])\
                    .single()\
                    .execute()
                
                if participant.data:
                    # Get student info
                    student = supabase.table('students')\
                        .select('*')\
                        .eq('id', participant.data['student_id'])\
                        .single()\
                        .execute()
                    
                    # Get week info
                    week = supabase.table('weeks')\
                        .select('week_number, topic')\
                        .eq('id', participant.data['week_id'])\
                        .single()\
                        .execute()
                    
                    score['participant'] = {
                        'student': {
                            'name': student.data.get('name') or student.data.get('full_name', 'Unknown'),
                            'roll_number': student.data.get('roll_number', 'N/A')
                        },
                        'week': week.data if week.data else {}
                    }
            except Exception as e:
                print(f"Error enriching score {score.get('id')}: {e}")
                score['participant'] = None
        
        return jsonify({'scores': response.data}), 200
    except Exception as e:
        print(f"Error in get_my_scores: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
