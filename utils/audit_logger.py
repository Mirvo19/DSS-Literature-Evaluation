"""
Audit logging utility for tracking admin actions
"""
from supabase import create_client
from config import Config
from flask import request
import json

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

class AuditLogger:
    """Helper class for creating audit log entries"""
    
    @staticmethod
    def log_action(admin_email, admin_id, action_type, entity_type, entity_id=None, 
                   entity_name=None, old_value=None, new_value=None, description=None):
        """
        Log an admin action to the audit_logs table
        
        Args:
            admin_email: Email of the admin performing the action
            admin_id: UUID of the admin user
            action_type: Type of action (CREATE, UPDATE, DELETE, etc.)
            entity_type: Type of entity (week, session, student, participant)
            entity_id: UUID of the affected entity
            entity_name: Human-readable name of the entity
            old_value: Dictionary of old values (for updates)
            new_value: Dictionary of new values
            description: Additional description of the action
        """
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
            # Don't fail the main operation if logging fails
    
    @staticmethod
    def get_current_user_info():
        """Get current user email from request headers"""
        try:
            # This would need to be implemented based on your auth system
            # For now, return a placeholder
            return "admin@example.com", None
        except:
            return "unknown", None
