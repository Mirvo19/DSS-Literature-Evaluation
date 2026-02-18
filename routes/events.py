from flask import Blueprint, request, jsonify
from supabase import create_client
from config import Config
from utils.auth import require_auth

bp = Blueprint('events', __name__)
api_bp = Blueprint('events_api', __name__, url_prefix='/api')

# page routes are in routes/en/ and routes/ne/
# service key needed for judge scores
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

@api_bp.route('/events', methods=['GET'])
def get_events():
    try:
        response = supabase.table('events').select('*').execute()
        return jsonify({'events': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/sessions/<event_id>', methods=['GET'])
@require_auth
def get_sessions(event_id):
    try:
        # filter by language
        language = request.args.get('lang', 'en')
        
        query = supabase.table('sessions')\
            .select('*')\
            .eq('event_id', event_id)\
            .eq('is_active', True)\
            .eq('language', language)\
            .order('session_number', desc=True)
        
        response = query.execute()
        
        return jsonify({'sessions': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/weeks/<session_id>', methods=['GET'])
@require_auth
def get_weeks(session_id):
    try:
        response = supabase.table('weeks')\
            .select('*, sessions!inner(event_id, session_number)')\
            .eq('session_id', session_id)\
            .order('week_number', desc=True)\
            .execute()
        
        return jsonify({'weeks': response.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/week-detail/<week_id>', methods=['GET'])
@require_auth
def get_week_detail(week_id):
    try:
        week_response = supabase.table('weeks')\
            .select('*, sessions!inner(session_number, name, event_id, events!inner(name, name_nepali))')\
            .eq('id', week_id)\
            .single()\
            .execute()
        
        participants_response = supabase.table('participants')\
            .select('*, students!inner(full_name, grade)')\
            .eq('week_id', week_id)\
            .order('score', desc=True)\
            .execute()
        
        judges_response = supabase.table('week_judges')\
            .select('*, judges!inner(full_name, title)')\
            .eq('week_id', week_id)\
            .execute()
        
        criteria_response = supabase.table('week_criteria')\
            .select('*, judging_criteria!inner(name, name_nepali, max_points)')\
            .eq('week_id', week_id)\
            .execute()
        
        return jsonify({
            'week': week_response.data,
            'participants': participants_response.data,
            'judges': judges_response.data,
            'criteria': criteria_response.data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/winners', methods=['GET'])
def get_winners():
    try:
        event_id = request.args.get('event_id')
        limit = request.args.get('limit', 50)
        
        # get weeks with winners
        query = supabase.table('weeks')\
            .select('id, week_number, topic, topic_nepali, date, sessions!inner(session_number, event_id, events!inner(name, name_nepali))')\
            .order('date', desc=True)\
            .limit(limit)
        
        if event_id:
            query = query.eq('sessions.event_id', event_id)
        
        weeks_response = query.execute()
        
        # Filter weeks that have winners
        weeks_with_winners = []
        for week in weeks_response.data:
            winners_check = supabase.table('participants')\
                .select('id', count='exact')\
                .eq('week_id', week['id'])\
                .eq('is_winner', True)\
                .execute()
            
            if winners_check.count and winners_check.count > 0:
                weeks_with_winners.append(week)
        
        return jsonify({'weeks': weeks_with_winners}), 200
        
    except Exception as e:
        print(f"Error in get_winners: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/week-rankings/<week_id>', methods=['GET'])
def get_week_rankings(week_id):
    try:
        print(f"Getting rankings for week: {week_id}")
        
        # get week info
        week = supabase.table('weeks')\
            .select('*, sessions!inner(session_number, events!inner(name, name_nepali))')\
            .eq('id', week_id)\
            .single()\
            .execute()
        
        print(f"Week info: {week.data}")
        
        # get participants
        participants = supabase.table('participants')\
            .select('id, student_id, position, is_winner')\
            .eq('week_id', week_id)\
            .execute()
        
        print(f"Found {len(participants.data)} participants")
        
        # Get student info and scores for each participant
        results = []
        for participant in participants.data:
            print(f"\nProcessing participant: {participant['id']}")
            
            student = supabase.table('students')\
                .select('*')\
                .eq('id', participant['student_id'])\
                .single()\
                .execute()
            
            # get scores
            scores = supabase.table('judge_scores')\
                .select('*')\
                .eq('participant_id', participant['id'])\
                .execute()
            
            print(f"Found {len(scores.data)} scores for participant {participant['id']}")
            print(f"Scores data: {scores.data}")
            
            # calculate scores by type
            overall_score = None
            content_score = None
            style_delivery_score = None
            language_score = None
            
            for score in scores.data:
                judge_type = score.get('judge_type')
                score_value = score.get('score')
                print(f"  Judge type: {judge_type}, Score: {score_value}")
                
                if judge_type == 'overall':
                    overall_score = score_value
                elif judge_type == 'content':
                    content_score = score_value
                elif judge_type == 'style_delivery':
                    style_delivery_score = score_value
                elif judge_type == 'language':
                    language_score = score_value
            
            # total score
            scores_list = [overall_score, content_score, style_delivery_score, language_score]
            filtered_scores = list(filter(None, scores_list))
            total_score = sum(filtered_scores) if filtered_scores else 0
            
            print(f"Scores list: {scores_list}")
            print(f"Filtered scores: {filtered_scores}")
            print(f"Calculated scores - Overall: {overall_score}, Content: {content_score}, Style/Delivery: {style_delivery_score}, Language: {language_score}, Total: {total_score}")
            
            results.append({
                'position': participant.get('position'),
                'is_winner': participant.get('is_winner', False),
                'student_name': student.data.get('full_name') or student.data.get('name', 'Unknown'),
                'roll_number': student.data.get('roll_number', 'N/A'),
                'grade': student.data.get('grade', 'N/A'),
                'overall_score': overall_score,
                'content_score': content_score,
                'style_delivery_score': style_delivery_score,
                'language_score': language_score,
                'total_score': total_score
            })
        
        # sort by position
        results.sort(key=lambda x: x['position'] if x['position'] else 999)
        
        print(f"\nReturning {len(results)} results")
        
        return jsonify({
            'week': week.data,
            'results': results
        }), 200
        
    except Exception as e:
        print(f"Error in get_week_rankings: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/weeks-by-event/<event_id>', methods=['GET'])
@require_auth
def get_weeks_by_event(event_id):
    try:
        # filter by language
        language = request.args.get('lang', 'en')
        
        sessions_response = supabase.table('sessions')\
            .select('id')\
            .eq('event_id', event_id)\
            .eq('is_active', True)\
            .eq('language', language)\
            .execute()
        
        if not sessions_response.data:
            return jsonify({'weeks': []}), 200
        
        session_ids = [s['id'] for s in sessions_response.data]
        
        weeks_response = supabase.table('weeks')\
            .select('*, sessions!inner(session_number, name)')\
            .in_('session_id', session_ids)\
            .order('date', desc=True)\
            .execute()
        
        return jsonify({'weeks': weeks_response.data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
