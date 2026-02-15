from flask import Blueprint, request, jsonify, render_template
from supabase import create_client
from config import Config
from utils.auth import require_admin
from utils.csv_handler import CSVStudentImporter
from utils.random_selector import ExtemporeRandomSelector
from utils.audit_logger import AuditLogger
import json

bp = Blueprint('admin', __name__, url_prefix='/admin')

# init supabase with service key
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

# pages

@bp.route('/dashboard')
def admin_dashboard_page():
    return render_template('admin/dashboard.html')

@bp.route('/students')
def admin_students_page():
    return render_template('admin/students.html')

@bp.route('/sessions')
def admin_sessions_page():
    return render_template('admin/sessions.html')

@bp.route('/weeks')
def admin_weeks_page():
    return render_template('admin/weeks.html')

@bp.route('/logs')
def admin_logs_page():
    return render_template('admin/logs.html')

@bp.route('/judge-permissions')
def admin_judge_permissions_page():
    return render_template('admin/judge_permissions.html')

@bp.route('/results')
def admin_results_page():
    return render_template('admin/results.html')

# student api

@bp.route('/api/students', methods=['GET'])
@require_admin
def get_all_students():
    try:
        response = supabase.table('students')\
            .select('*')\
            .order('full_name')\
            .execute()
        
        return jsonify({'students': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/students', methods=['POST'])
@require_admin
def create_student():
    try:
        data = request.json
        
        if not data.get('full_name'):
            return jsonify({'error': 'Student name is required'}), 400
        
        response = supabase.table('students').insert({
            'full_name': data['full_name'],
            'grade': data.get('grade'),
            'email': data.get('email'),
            'is_active': data.get('is_active', True)
        }).execute()
        
        return jsonify({'student': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/students/<student_id>', methods=['PUT'])
@require_admin
def update_student(student_id):
    # code
    try:
        data = request.json
        
        update_data = {}
        if 'full_name' in data:
            update_data['full_name'] = data['full_name']
        if 'grade' in data:
            update_data['grade'] = data['grade']
        if 'email' in data:
            update_data['email'] = data['email']
        if 'is_active' in data:
            update_data['is_active'] = data['is_active']
        
        response = supabase.table('students')\
            .update(update_data)\
            .eq('id', student_id)\
            .execute()
        
        return jsonify({'student': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/students/<student_id>', methods=['DELETE'])
@require_admin
def delete_student(student_id):
    # code
    try:
        supabase.table('students').delete().eq('id', student_id).execute()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# CSV IMPORT
# ============================================

@bp.route('/api/import-csv', methods=['POST'])
@require_admin
def import_students_csv():
    # code
    try:
        data = request.json
        csv_content = data.get('csv_content')
        
        if not csv_content:
            return jsonify({'error': 'No CSV content provided'}), 400
        
        # code
        students, parse_errors = CSVStudentImporter.parse_csv(csv_content)
        
        if parse_errors and not students:
            return jsonify({
                'error': 'CSV parsing failed',
                'errors': parse_errors
            }), 400
        
        # code
        existing = supabase.table('students').select('full_name').execute()
        
        # code
        valid_students, warnings = CSVStudentImporter.validate_against_database(
            students, 
            existing.data
        )
        
        # code
        imported_count = 0
        import_errors = []
        
        if valid_students:
            try:
                response = supabase.table('students').insert(valid_students).execute()
                imported_count = len(response.data)
            except Exception as e:
                import_errors.append(f"Database import error: {str(e)}")
        
        # code
        summary = CSVStudentImporter.generate_import_summary(
            total_rows=len(students),
            imported=imported_count,
            skipped=len(students) - len(valid_students),
            errors=parse_errors + warnings + import_errors
        )
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': f'Import failed: {str(e)}'}), 500

# ============================================
# SESSION MANAGEMENT
# ============================================

@bp.route('/api/sessions', methods=['GET'])
@require_admin
def get_all_sessions():
    # code
    try:
        response = supabase.table('sessions')\
            .select('*, events!inner(name, name_nepali)')\
            .order('created_at', desc=True)\
            .execute()
        
        return jsonify({'sessions': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/sessions', methods=['POST'])
@require_admin
def create_session():
    # code
    try:
        data = request.json
        
        if not data.get('event_id') or not data.get('name'):
            return jsonify({'error': 'Event ID and name are required'}), 400
        
        response = supabase.table('sessions').insert({
            'event_id': data['event_id'],
            'name': data['name'],
            'session_number': data.get('session_number', 1),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'is_active': data.get('is_active', True)
        }).execute()
        
        return jsonify({'session': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/sessions/<session_id>', methods=['PUT'])
@require_admin
def update_session(session_id):
    # code
    try:
        data = request.json
        
        update_data = {}
        for field in ['name', 'session_number', 'start_date', 'end_date', 'is_active']:
            if field in data:
                update_data[field] = data[field]
        
        response = supabase.table('sessions')\
            .update(update_data)\
            .eq('id', session_id)\
            .execute()
        
        return jsonify({'session': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/sessions/<session_id>', methods=['DELETE'])
@require_admin
def delete_session(session_id):
    # code
    try:
        supabase.table('sessions').delete().eq('id', session_id).execute()
        return jsonify({'message': 'Session deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# WEEK MANAGEMENT
# ============================================

@bp.route('/api/weeks', methods=['GET'])
@require_admin
def get_all_weeks():
    # code
    try:
        response = supabase.table('weeks')\
            .select('*, sessions!inner(session_number, name, events!inner(name))')\
            .order('created_at', desc=True)\
            .execute()
        
        return jsonify({'weeks': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/weeks', methods=['POST'])
@require_admin
def create_week():
    # code
    try:
        data = request.json
        print(f"Create week request data: {data}")  # Debug logging
        
        if not data.get('session_id') or not data.get('week_number'):
            return jsonify({'error': 'Session ID and week number are required'}), 400
        
        session_id = data['session_id']
        week_number = data['week_number']
        
        # code
        week_data = {
            'session_id': session_id,
            'week_number': week_number,
            'topic': data.get('topic'),
            'date': data.get('date'),
            'is_partial': data.get('is_partial', False),
            'notes': data.get('notes')
        }
        
        week_response = supabase.table('weeks').insert(week_data).execute()
        week_id = week_response.data[0]['id']
        
        # Log the action
        admin_email, admin_id = get_admin_email_from_request()
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='CREATE',
            entity_type='week',
            entity_id=week_id,
            entity_name=f"Week {week_number} - {data.get('topic', 'No Topic')}",
            new_value=week_data,
            description=f"Created week {week_number} for session {session_id}"
        )
        
        # code
        participant_mode = data.get('participant_mode', 'manual')
        
        if participant_mode == 'random':
            # Random selection for Extempore
            result = _handle_random_selection(
                week_id=week_id,
                session_id=session_id,
                participant_count=data.get('participant_count', 5),
                grade_filter=data.get('grade_filter'),
                reset_if_insufficient=data.get('reset_if_insufficient', False)
            )
            
            return jsonify({
                'week': week_response.data[0],
                'selection_result': result
            }), 201
            
        elif participant_mode == 'manual' and data.get('student_ids'):
            # code
            participants = [
                {
                    'week_id': week_id,
                    'student_id': student_id,
                    'score': 0,
                    'is_winner': False
                }
                for student_id in data['student_ids']
            ]
            
            supabase.table('participants').insert(participants).execute()
            
            # code
            _mark_students_as_spoken(session_id, data['student_ids'], week_id)
        
        return jsonify({'week': week_response.data[0]}), 201
        
    except Exception as e:
        print(f"Error creating week: {e}")  # Debug logging
        import traceback
        traceback.print_exc()  # Print full traceback
        return jsonify({'error': str(e)}), 500

def _handle_random_selection(week_id, session_id, participant_count, grade_filter, reset_if_insufficient):
    # code
    try:
        # code
        students_response = supabase.table('students')\
            .select('*')\
            .eq('is_active', True)\
            .execute()
        
        # code
        status_response = supabase.table('session_speaker_status')\
            .select('*')\
            .eq('session_id', session_id)\
            .execute()
        
        # code
        available_students = ExtemporeRandomSelector.get_available_students(
            all_students=students_response.data,
            session_id=session_id,
            speaker_status=status_response.data,
            grade_filter=grade_filter
        )
        
        # code
        is_sufficient, message, recommendation = ExtemporeRandomSelector.check_availability(
            len(available_students),
            participant_count
        )
        
        # code
        if not is_sufficient:
            if reset_if_insufficient and recommendation == "partial_or_reset":
                # code
                _reset_session_speakers(session_id)
                return _handle_random_selection(
                    week_id, session_id, participant_count, grade_filter, False
                )
            elif len(available_students) > 0:
                # code
                participant_count = len(available_students)
                supabase.table('weeks')\
                    .update({'is_partial': True})\
                    .eq('id', week_id)\
                    .execute()
            else:
                return {
                    'success': False,
                    'message': message,
                    'recommendation': recommendation
                }
        
        # code
        selected_students = ExtemporeRandomSelector.select_random_participants(
            available_students,
            participant_count
        )
        
        # code
        is_valid, error = ExtemporeRandomSelector.validate_selection(selected_students)
        if not is_valid:
            return {'success': False, 'message': error}
        
        # code
        participant_records = ExtemporeRandomSelector.prepare_participant_records(
            week_id,
            selected_students
        )
        
        supabase.table('participants').insert(participant_records).execute()
        
        # code
        student_ids = [s['id'] for s in selected_students]
        _mark_students_as_spoken(session_id, student_ids, week_id)
        
        return {
            'success': True,
            'message': f'Selected {len(selected_students)} participants',
            'participant_count': len(selected_students),
            'is_partial': len(selected_students) < participant_count
        }
        
    except Exception as e:
        return {'success': False, 'message': f'Selection error: {str(e)}'}

def _mark_students_as_spoken(session_id, student_ids, week_id):
    # code
    try:
        # code
        existing = supabase.table('session_speaker_status')\
            .select('*')\
            .eq('session_id', session_id)\
            .in_('student_id', student_ids)\
            .execute()
        
        existing_student_ids = {record['student_id'] for record in existing.data}
        
        # code
        if existing.data:
            for student_id in existing_student_ids:
                supabase.table('session_speaker_status')\
                    .update({
                        'has_spoken': True,
                        'spoken_in_week_id': week_id
                    })\
                    .eq('session_id', session_id)\
                    .eq('student_id', student_id)\
                    .execute()
        
        # code
        new_student_ids = set(student_ids) - existing_student_ids
        if new_student_ids:
            new_records = [
                {
                    'session_id': session_id,
                    'student_id': student_id,
                    'has_spoken': True,
                    'spoken_in_week_id': week_id
                }
                for student_id in new_student_ids
            ]
            supabase.table('session_speaker_status').insert(new_records).execute()
            
    except Exception as e:
        print(f"Error marking students as spoken: {e}")

def _reset_session_speakers(session_id):
    # code
    try:
        supabase.table('session_speaker_status')\
            .update({
                'has_spoken': False,
                'spoken_in_week_id': None
            })\
            .eq('session_id', session_id)\
            .execute()
    except Exception as e:
        print(f"Error resetting speakers: {e}")

@bp.route('/api/weeks/<week_id>', methods=['GET'])
@require_admin
def get_week_details(week_id):
    # code
    try:
        # Get week details with session and event info
        week_response = supabase.table('weeks')\
            .select('*, sessions!inner(session_number, name, events!inner(name, name_nepali))')\
            .eq('id', week_id)\
            .execute()
        
        if not week_response.data:
            return jsonify({'error': 'Week not found'}), 404
        
        week = week_response.data[0]
        
        # Get participants with student details
        participants_response = supabase.table('participants')\
            .select('*, students!inner(full_name, grade)')\
            .eq('week_id', week_id)\
            .execute()
        
        week['participants'] = participants_response.data
        
        return jsonify({'week': week}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/weeks/<week_id>', methods=['PUT'])
@require_admin
def update_week(week_id):
    # code
    try:
        data = request.json
        
        update_data = {}
        for field in ['week_number', 'topic', 'date', 'is_partial', 'notes']:
            if field in data:
                update_data[field] = data[field]
        
        response = supabase.table('weeks')\
            .update(update_data)\
            .eq('id', week_id)\
            .execute()
        
        return jsonify({'week': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/weeks/<week_id>', methods=['DELETE'])
@require_admin
def delete_week(week_id):
    # code
    try:
        supabase.table('weeks').delete().eq('id', week_id).execute()
        return jsonify({'message': 'Week deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/weeks/<week_id>/add-random-participants', methods=['POST'])
@require_admin
def add_random_participants_to_week(week_id):
    """Add random participants to an existing week"""
    try:
        data = request.json
        
        # Get week details to get session_id
        week = supabase.table('weeks').select('session_id').eq('id', week_id).execute()
        if not week.data:
            return jsonify({'error': 'Week not found'}), 404
        
        session_id = week.data[0]['session_id']
        participant_count = data.get('participant_count', 5)
        grade_filter = data.get('grade_filter')
        reset_if_insufficient = data.get('reset_if_insufficient', False)
        
        # Use the existing random selection logic
        result = _handle_random_selection(
            week_id=week_id,
            session_id=session_id,
            participant_count=participant_count,
            grade_filter=grade_filter,
            reset_if_insufficient=reset_if_insufficient
        )
        
        # Log the action
        admin_email, admin_id = get_admin_email_from_request()
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='UPDATE',
            entity_type='week',
            entity_id=week_id,
            entity_name=f"Week {week_id}",
            new_value={'added_random_participants': participant_count},
            description=f"Added {participant_count} random participants to week"
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# RESET SESSION SPEAKERS
# ============================================

@bp.route('/api/sessions/<session_id>/reset-speakers', methods=['POST'])
@require_admin
def reset_session_speakers(session_id):
    # code
    try:
        _reset_session_speakers(session_id)
        return jsonify({'message': 'Session speakers reset successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# PARTICIPANT MANAGEMENT
# ============================================

@bp.route('/api/participants/<participant_id>', methods=['PUT'])
@require_admin
def update_participant(participant_id):
    # code
    try:
        data = request.json
        
        update_data = {}
        if 'score' in data:
            update_data['score'] = data['score']
        if 'is_winner' in data:
            update_data['is_winner'] = data['is_winner']
        if 'position' in data:
            update_data['position'] = data['position']
        if 'notes' in data:
            update_data['notes'] = data['notes']
        
        response = supabase.table('participants')\
            .update(update_data)\
            .eq('id', participant_id)\
            .execute()
        
        return jsonify({'participant': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/participants', methods=['POST'])
@require_admin
def add_participant():
    # code
    try:
        data = request.json
        
        if not data.get('week_id') or not data.get('student_id'):
            return jsonify({'error': 'Week ID and Student ID are required'}), 400
        
        response = supabase.table('participants').insert({
            'week_id': data['week_id'],
            'student_id': data['student_id'],
            'score': data.get('score', 0),
            'is_winner': data.get('is_winner', False),
            'position': data.get('position'),
            'notes': data.get('notes')
        }).execute()
        
        # Log the action
        admin_email, admin_id = get_admin_email_from_request()
        student = supabase.table('students').select('full_name').eq('id', data['student_id']).execute()
        student_name = student.data[0]['full_name'] if student.data else 'Unknown'
        
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='CREATE',
            entity_type='participant',
            entity_id=response.data[0]['id'],
            entity_name=student_name,
            new_value={'student_id': data['student_id'], 'week_id': data['week_id']},
            description=f"Added participant {student_name} to week"
        )
        
        return jsonify({'participant': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/participants/<participant_id>', methods=['DELETE'])
@require_admin
def remove_participant(participant_id):
    # code
    try:
        # Get participant info before deleting
        participant = supabase.table('participants')\
            .select('*, students(full_name)')\
            .eq('id', participant_id)\
            .execute()
        
        supabase.table('participants').delete().eq('id', participant_id).execute()
        
        # Log the action
        admin_email, admin_id = get_admin_email_from_request()
        student_name = participant.data[0]['students']['full_name'] if participant.data else 'Unknown'
        
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='DELETE',
            entity_type='participant',
            entity_id=participant_id,
            entity_name=student_name,
            old_value=participant.data[0] if participant.data else None,
            description=f"Removed participant {student_name}"
        )
        
        return jsonify({'message': 'Participant removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# JUDGE MANAGEMENT
# ============================================

@bp.route('/api/judges', methods=['GET'])
@require_admin
def get_all_judges():
    # code
    try:
        response = supabase.table('judges')\
            .select('*')\
            .order('full_name')\
            .execute()
        
        return jsonify({'judges': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/judges', methods=['POST'])
@require_admin
def create_judge():
    # code
    try:
        data = request.json
        
        if not data.get('full_name'):
            return jsonify({'error': 'Judge name is required'}), 400
        
        response = supabase.table('judges').insert({
            'full_name': data['full_name'],
            'title': data.get('title'),
            'email': data.get('email'),
            'is_active': data.get('is_active', True)
        }).execute()
        
        return jsonify({'judge': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/judges/<judge_id>', methods=['PUT'])
@require_admin
def update_judge(judge_id):
    # code
    try:
        data = request.json
        
        update_data = {}
        for field in ['full_name', 'title', 'email', 'is_active']:
            if field in data:
                update_data[field] = data[field]
        
        response = supabase.table('judges')\
            .update(update_data)\
            .eq('id', judge_id)\
            .execute()
        
        return jsonify({'judge': response.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/judges/<judge_id>', methods=['DELETE'])
@require_admin
def delete_judge(judge_id):
    # code
    try:
        supabase.table('judges').delete().eq('id', judge_id).execute()
        return jsonify({'message': 'Judge deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# WEEK JUDGES & CRITERIA
# ============================================

@bp.route('/api/weeks/<week_id>/judges', methods=['POST'])
@require_admin
def assign_judge_to_week(week_id):
    # code
    try:
        data = request.json
        
        if not data.get('judge_id'):
            return jsonify({'error': 'Judge ID is required'}), 400
        
        response = supabase.table('week_judges').insert({
            'week_id': week_id,
            'judge_id': data['judge_id']
        }).execute()
        
        return jsonify({'week_judge': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/weeks/<week_id>/criteria', methods=['POST'])
@require_admin
def assign_criteria_to_week(week_id):
    # code
    try:
        data = request.json
        
        if not data.get('criteria_id'):
            return jsonify({'error': 'Criteria ID is required'}), 400
        
        response = supabase.table('week_criteria').insert({
            'week_id': week_id,
            'criteria_id': data['criteria_id']
        }).execute()
        
        return jsonify({'week_criteria': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/judging-criteria', methods=['GET'])
@require_admin
def get_all_criteria():
    # code
    try:
        response = supabase.table('judging_criteria')\
            .select('*')\
            .order('name')\
            .execute()
        
        return jsonify({'criteria': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# AUDIT LOGS
# ============================================

@bp.route('/api/audit-logs', methods=['GET'])
@require_admin
def get_audit_logs():
    """Get all audit logs with optional filtering"""
    try:
        query = supabase.table('audit_logs').select('*')
        
        # Apply filters if provided
        action_type = request.args.get('action_type')
        entity_type = request.args.get('entity_type')
        admin_email = request.args.get('admin_email')
        limit = request.args.get('limit', 100)
        
        if action_type:
            query = query.eq('action_type', action_type)
        if entity_type:
            query = query.eq('entity_type', entity_type)
        if admin_email:
            query = query.ilike('admin_email', f'%{admin_email}%')
        
        response = query.order('created_at', desc=True).limit(limit).execute()
        
        return jsonify({'logs': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_admin_email_from_request():
    """Extract admin email from the current request"""
    try:
        # Get the authorization token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            # Use supabase to get user info from token
            user = supabase.auth.get_user(token)
            if user and user.user:
                return user.user.email, user.user.id
        return 'unknown@admin.com', None
    except Exception as e:
        print(f"Error getting admin email: {e}")
        return 'unknown@admin.com', None

# ============================================
# JUDGE PERMISSIONS MANAGEMENT
# ============================================

@bp.route('/api/judge-permissions', methods=['GET'])
@require_admin
def get_judge_permissions():
    """Get all judge permissions"""
    try:
        response = supabase.table('judge_permissions')\
            .select('*')\
            .order('granted_at', desc=True)\
            .execute()
        
        # Fetch week details separately for each permission
        for permission in response.data:
            if permission.get('week_id'):
                try:
                    week = supabase.table('weeks')\
                        .select('week_number, topic, session_id')\
                        .eq('id', permission['week_id'])\
                        .single()\
                        .execute()
                    if week.data:
                        permission['week'] = week.data
                except:
                    permission['week'] = None
        
        return jsonify({'permissions': response.data}), 200
    except Exception as e:
        print(f"Error in get_judge_permissions: {e}")
        error_msg = str(e)
        if 'relation "judge_permissions" does not exist' in error_msg or 'table' in error_msg.lower():
            return jsonify({
                'error': 'Judge permissions table not found. Please run the database migration first.',
                'migration_file': 'database/migration_judge_permissions.sql',
                'details': error_msg
            }), 500
        return jsonify({'error': error_msg}), 500

@bp.route('/api/judge-permissions', methods=['POST'])
@require_admin
def grant_judge_permission():
    """Grant judging permission to a user for a specific week"""
    try:
        data = request.json
        admin_email, admin_id = get_admin_email_from_request()
        
        if not data.get('user_email') or not data.get('week_id') or not data.get('judge_type'):
            return jsonify({'error': 'User email, week ID, and judge type are required'}), 400
        
        response = supabase.table('judge_permissions').insert({
            'user_email': data['user_email'],
            'week_id': data['week_id'],
            'judge_type': data['judge_type'],
            'granted_by_admin_email': admin_email,
            'is_active': True
        }).execute()
        
        # Log the action
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='CREATE',
            entity_type='judge_permission',
            entity_id=response.data[0]['id'],
            entity_name=f"{data['user_email']} - {data['judge_type']}",
            new_value=data,
            description=f"Granted {data['judge_type']} permission to {data['user_email']}"
        )
        
        return jsonify({'permission': response.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/judge-permissions/<permission_id>/revoke', methods=['POST'])
@require_admin
def revoke_judge_permission(permission_id):
    """Revoke a judge permission"""
    try:
        admin_email, admin_id = get_admin_email_from_request()
        
        response = supabase.table('judge_permissions')\
            .update({
                'is_active': False,
                'revoked_at': 'NOW()',
                'revoked_by_admin_email': admin_email
            })\
            .eq('id', permission_id)\
            .execute()
        
        # Log the action
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='UPDATE',
            entity_type='judge_permission',
            entity_id=permission_id,
            description=f"Revoked judge permission"
        )
        
        return jsonify({'message': 'Permission revoked successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/judge-permissions/<permission_id>/reactivate', methods=['POST'])
@require_admin
def reactivate_judge_permission(permission_id):
    """Reactivate a revoked judge permission"""
    try:
        admin_email, admin_id = get_admin_email_from_request()
        
        response = supabase.table('judge_permissions')\
            .update({
                'is_active': True,
                'revoked_at': None,
                'revoked_by_admin_email': None
            })\
            .eq('id', permission_id)\
            .execute()
        
        # Log the action
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='UPDATE',
            entity_type='judge_permission',
            entity_id=permission_id,
            description=f"Re-activated judge permission"
        )
        
        return jsonify({'message': 'Permission re-activated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# RESULTS & WINNERS
# ============================================

@bp.route('/api/results/<week_id>', methods=['GET'])
@require_admin
def get_week_results(week_id):
    """Get aggregated results for a specific week"""
    try:
        # Get all participants for this week
        participants = supabase.table('participants')\
            .select('id, student_id')\
            .eq('week_id', week_id)\
            .execute()
        
        print(f"Fetched {len(participants.data)} participants for week {week_id}")
        
        results = []
        
        for participant in participants.data:
            participant_id = participant['id']
            student_id = participant['student_id']
            
            # Get student data separately
            try:
                student_response = supabase.table('students')\
                    .select('*')\
                    .eq('id', student_id)\
                    .single()\
                    .execute()
                student = student_response.data
            except Exception as student_error:
                print(f"Error fetching student {student_id}: {student_error}")
                continue
            
            if not student:
                print(f"Warning: No student data for participant {participant_id}")
                continue
            
            # Get all scores for this participant
            try:
                scores = supabase.table('judge_scores')\
                    .select('*')\
                    .eq('participant_id', participant_id)\
                    .execute()
                print(f"Fetched {len(scores.data)} scores for participant {participant_id}")
                if scores.data:
                    for score in scores.data:
                        print(f"  Score: {score}")
            except Exception as score_error:
                # If judge_scores table doesn't exist, return empty scores
                print(f"Error fetching scores: {score_error}")
                scores = type('obj', (object,), {'data': []})()
            
            # Aggregate scores by judge type
            overall_score = None
            content_score = None
            style_delivery_score = None
            language_score = None
            
            for score in scores.data:
                judge_type = score.get('judge_type')
                if judge_type == 'overall':
                    overall_score = score.get('score')
                elif judge_type == 'content':
                    content_score = score.get('score')
                elif judge_type == 'style_delivery':
                    style_delivery_score = score.get('score')
                elif judge_type == 'language':
                    language_score = score.get('score')
            
            # Calculate total score (sum of all judge types)
            total_score = sum(filter(None, [overall_score, content_score, style_delivery_score, language_score]))
            
            # Use full_name if name doesn't exist
            student_name = student.get('name') or student.get('full_name', 'Unknown')
            
            results.append({
                'participant_id': participant_id,
                'student_name': student_name,
                'roll_number': student.get('roll_number', 'N/A'),
                'overall_score': overall_score,
                'content_score': content_score,
                'style_delivery_score': style_delivery_score,
                'language_score': language_score,
                'total_score': total_score
            })
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        print(f"Returning {len(results)} results")
        return jsonify({'results': results}), 200
    except Exception as e:
        print(f"Error in get_week_results: {e}")
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        if 'relation "judge_scores" does not exist' in error_msg or 'table' in error_msg.lower():
            return jsonify({
                'results': [],
                'message': 'Judging system not yet configured. Please run the database migration.'
            }), 200
        return jsonify({'error': error_msg}), 500

@bp.route('/api/participant/<participant_id>/scores', methods=['GET'])
@require_admin
def get_participant_scores(participant_id):
    """Get detailed scores for a specific participant"""
    try:
        # Get participant info
        participant = supabase.table('participants')\
            .select('id, student_id')\
            .eq('id', participant_id)\
            .single()\
            .execute()
        
        if not participant.data:
            return jsonify({'error': 'Participant not found'}), 404
        
        # Get student data separately
        student = supabase.table('students')\
            .select('*')\
            .eq('id', participant.data['student_id'])\
            .single()\
            .execute()
        
        # Get all scores
        scores = supabase.table('judge_scores')\
            .select('*')\
            .eq('participant_id', participant_id)\
            .execute()
        
        student_name = student.data.get('name') or student.data.get('full_name', 'Unknown')
        
        return jsonify({
            'student_name': student_name,
            'roll_number': student.data.get('roll_number', 'N/A'),
            'scores': scores.data
        }), 200
    except Exception as e:
        print(f"Error in get_participant_scores: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/publish-winners/<week_id>', methods=['POST'])
@require_admin
def publish_winners(week_id):
    """Publish the top 3 winners for a specific week"""
    try:
        admin_email, admin_id = get_admin_email_from_request()
        
        # Get all participants for this week with their scores
        participants = supabase.table('participants')\
            .select('id, student_id')\
            .eq('week_id', week_id)\
            .execute()
        
        if not participants.data:
            return jsonify({'error': 'No participants found for this week'}), 404
        
        # Calculate scores for all participants
        results = []
        for participant in participants.data:
            participant_id = participant['id']
            
            # Get all scores for this participant
            scores = supabase.table('judge_scores')\
                .select('*')\
                .eq('participant_id', participant_id)\
                .execute()
            
            # Aggregate scores by judge type
            total_score = 0
            for score in scores.data:
                total_score += score.get('score', 0)
            
            results.append({
                'participant_id': participant_id,
                'total_score': total_score
            })
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        if len(results) == 0:
            return jsonify({'error': 'No scores available to determine winners'}), 400
        
        # First, clear all existing winners for this week
        supabase.table('participants')\
            .update({'is_winner': False})\
            .eq('week_id', week_id)\
            .execute()
        
        # Mark all participants with their positions
        # Top 3 get is_winner = True, all get their rank
        published_count = 0
        for index, result in enumerate(results):
            position = index + 1
            is_winner = position <= 3
            
            supabase.table('participants')\
                .update({
                    'is_winner': is_winner,
                    'position': position
                })\
                .eq('id', result['participant_id'])\
                .execute()
            published_count += 1
        
        # Log this action
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='UPDATE',
            entity_type='week',
            entity_id=week_id,
            entity_name=f"Week Results Published",
            new_value={'published_count': published_count, 'total_participants': len(results)},
            description=f"Published results and rankings for {published_count} participants"
        )
        
        return jsonify({
            'message': 'Winners published successfully',
            'published_count': published_count
        }), 200
        
    except Exception as e:
        print(f"Error in publish_winners: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/week/<week_id>/publish-status', methods=['GET'])
@require_admin
def get_publish_status(week_id):
    """Check if a week's results are published"""
    try:
        # Check if any participants are marked as winners
        winners = supabase.table('participants')\
            .select('id', count='exact')\
            .eq('week_id', week_id)\
            .eq('is_winner', True)\
            .execute()
        
        is_published = winners.count and winners.count > 0
        
        return jsonify({'is_published': is_published}), 200
        
    except Exception as e:
        print(f"Error checking publish status: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/unpublish-winners/<week_id>', methods=['POST'])
@require_admin
def unpublish_winners(week_id):
    """Unpublish/revoke the winners for a specific week"""
    try:
        admin_email, admin_id = get_admin_email_from_request()
        
        # Get count before unpublishing
        winners = supabase.table('participants')\
            .select('id', count='exact')\
            .eq('week_id', week_id)\
            .eq('is_winner', True)\
            .execute()
        
        unpublished_count = winners.count or 0
        
        # Clear all winners and positions for this week
        supabase.table('participants')\
            .update({'is_winner': False, 'position': None})\
            .eq('week_id', week_id)\
            .execute()
        
        # Log this action
        AuditLogger.log_action(
            admin_email=admin_email,
            admin_id=admin_id,
            action_type='UPDATE',
            entity_type='week',
            entity_id=week_id,
            entity_name=f"Week Results Unpublished",
            old_value={'unpublished_count': unpublished_count},
            description=f"Unpublished results for {unpublished_count} participants"
        )
        
        return jsonify({
            'message': 'Results unpublished successfully',
            'unpublished_count': unpublished_count
        }), 200
        
    except Exception as e:
        print(f"Error in unpublish_winners: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
