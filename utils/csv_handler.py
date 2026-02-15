import csv
import io
from typing import List, Dict, Tuple

class CSVStudentImporter:
    
    @staticmethod
    def parse_csv(file_content: str) -> Tuple[List[Dict], List[str]]:
        students = []
        errors = []
        
        try:
            csv_file = io.StringIO(file_content)
            reader = csv.DictReader(csv_file)
            
            # validate headers
            expected_headers = {'full_name', 'grade'}
            if not expected_headers.issubset(set(reader.fieldnames)):
                errors.append(f"CSV must contain headers: {', '.join(expected_headers)}")
                return students, errors
            
            line_number = 1
            seen_names = set()
            
            for row in reader:
                line_number += 1
                
                name = row.get('full_name', '').strip()
                if not name:
                    errors.append(f"Line {line_number}: Missing student name")
                    continue
                
                # check duplicates
                if name.lower() in seen_names:
                    errors.append(f"Line {line_number}: Duplicate student '{name}' in CSV")
                    continue
                
                seen_names.add(name.lower())
                
                # validate grade
                grade = row.get('grade', '').strip()
                grade_int = None
                
                if grade:
                    try:
                        grade_int = int(grade)
                        if grade_int < 1 or grade_int > 12:
                            errors.append(f"Line {line_number}: Invalid grade '{grade}' for {name} (must be 1-12)")
                            continue
                    except ValueError:
                        errors.append(f"Line {line_number}: Invalid grade '{grade}' for {name} (must be a number)")
                        continue
                
                students.append({
                    'full_name': name,
                    'grade': grade_int,
                    'email': row.get('email', '').strip() or None,
                    'is_active': True
                })
            
            return students, errors
            
        except Exception as e:
            errors.append(f"CSV parsing error: {str(e)}")
            return students, errors
    
    @staticmethod
    def validate_against_database(students: List[Dict], existing_students: List[Dict]) -> Tuple[List[Dict], List[str]]:
        valid_students = []
        warnings = []
        
        existing_names = {s['full_name'].lower() for s in existing_students}
        
        for student in students:
            name_lower = student['full_name'].lower()
            
            if name_lower in existing_names:
                warnings.append(f"Student '{student['full_name']}' already exists in database - skipping")
            else:
                valid_students.append(student)
                existing_names.add(name_lower)
        
        return valid_students, warnings
    
    @staticmethod
    def generate_import_summary(total_rows: int, imported: int, skipped: int, errors: List[str]) -> Dict:
        return {
            'total_rows': total_rows,
            'imported': imported,
            'skipped': skipped,
            'errors': errors,
            'success': len(errors) == 0 or imported > 0
        }
