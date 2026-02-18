# audit logging for admin actions
from supabase import create_client
from config import Config
from flask import request
import json

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

class AuditLogger:
    
    @staticmethod
    def log_action(admin_email, admin_id, action_type, entity_type, entity_id=None, 
                   entity_name=None, old_value=None, new_value=None, description=None):
        try:
            log_entry = {
                'admin_email': admin_email,
                'admin_id': admin_id,
                'action_type': action_type,
                'entity_type': entity_type,
                'entity_id': entity_id,
                'entity_name': entity_name,
                'old_value': json.dumps(old_value) if old_value else None,
                'new_value': json.dumps(new_value) if new_value else None,
                'description': description
            }
            
            supabase.table('audit_logs').insert(log_entry).execute()
        except Exception as e:
            print(f"Error logging audit entry: {e}")
            # don't fail main if logging fails
    
    @staticmethod
    def get_current_user_info():
        try:
            return "admin@example.com", None
        except:
            return "unknown", None
