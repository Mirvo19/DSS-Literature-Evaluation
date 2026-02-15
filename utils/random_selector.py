import random
from typing import List, Dict, Tuple, Optional

class ExtemporeRandomSelector:
    
    @staticmethod
    def get_available_students(
        all_students: List[Dict],
        session_id: str,
        speaker_status: List[Dict],
        grade_filter: Optional[int] = None
    ) -> List[Dict]:
        # find who spoke
        spoken_student_ids = {
            status['student_id'] 
            for status in speaker_status 
            if status['session_id'] == session_id and status['has_spoken']
        }
        
        # filter students
        available = []
        for student in all_students:
            if student['id'] in spoken_student_ids:
                continue
            
            if not student.get('is_active', True):
                continue
            
            if grade_filter is not None:
                if student.get('grade') != grade_filter:
                    continue
            
            available.append(student)
        
        return available
    
    @staticmethod
    def select_random_participants(
        available_students: List[Dict],
        count: int,
        seed: Optional[int] = None
    ) -> List[Dict]:
        if seed is not None:
            random.seed(seed)
        
        if len(available_students) <= count:
            return available_students.copy()
        
        return random.sample(available_students, count)
    
    @staticmethod
    def check_availability(
        available_count: int,
        required_count: int
    ) -> Tuple[bool, str, Optional[str]]:
        if available_count >= required_count:
            return True, f"{available_count} students available", None
        
        elif available_count > 0:
            return False, f"Only {available_count} students available (need {required_count})", "partial_or_reset"
        
        else:
            return False, "No students available", "reset_required"
    
    @staticmethod
    def create_speaker_status_records(
        session_id: str,
        student_ids: List[str],
        week_id: str
    ) -> List[Dict]:
        records = []
        for student_id in student_ids:
            records.append({
                'session_id': session_id,
                'student_id': student_id,
                'has_spoken': True,
                'spoken_in_week_id': week_id
            })
        
        return records
    
    @staticmethod
    def reset_session_speakers(
        session_id: str
    ) -> Dict:
        return {
            'session_id': session_id,
            'reset_values': {
                'has_spoken': False,
                'spoken_in_week_id': None
            }
        }
    
    @staticmethod
    def validate_selection(
        selected_students: List[Dict],
        minimum_required: int = 1
    ) -> Tuple[bool, Optional[str]]:
        # code
        if len(selected_students) < minimum_required:
            return False, f"Need at least {minimum_required} participant(s)"
        
        # code
        student_ids = [s['id'] for s in selected_students]
        if len(student_ids) != len(set(student_ids)):
            return False, "Duplicate students in selection"
        
        return True, None
    
    @staticmethod
    def prepare_participant_records(
        week_id: str,
        selected_students: List[Dict]
    ) -> List[Dict]:
        # code
        participants = []
        for student in selected_students:
            participants.append({
                'week_id': week_id,
                'student_id': student['id'],
                'score': 0,
                'is_winner': False,
                'position': None,
                'notes': None
            })
        
        return participants
