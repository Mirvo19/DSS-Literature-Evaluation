from functools import wraps
from flask import request, jsonify, redirect
from supabase import create_client
from config import Config
import jwt

# init supabase
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
supabase_admin = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

def get_user_from_token(token):
    try:
        user = supabase.auth.get_user(token)
        return user.user if user else None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'No authorization token provided'}), 401
        
        # strip bearer
        if token.startswith('Bearer '):
            token = token[7:]
        
        user = get_user_from_token(token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # attach user to request
        request.user = user
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # try auth header first
        token = request.headers.get('Authorization')
        
        if token and token.startswith('Bearer '):
            token = token[7:]
        elif not token:
            # fall back to cookie
            token = request.cookies.get('access_token')
        
        # check if it's a page request
        is_html_request = 'text/html' in request.headers.get('Accept', '')
        
        if not token:
            if is_html_request:
                # no token, redirect to login
                return redirect('/')
            return jsonify({'error': 'No authorization token provided'}), 401
        
        user = get_user_from_token(token)
        
        if not user:
            if is_html_request:
                return redirect('/')
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # check admin table
        try:
            result = supabase_admin.table('admins').select('*').eq('user_id', user.id).execute()
            
            if not result.data or len(result.data) == 0:
                if is_html_request:
                    # not admin, send back to login
                    return redirect('/')
                return jsonify({'error': 'Unauthorized. Admin access required.'}), 403
            
            request.user = user
            request.is_admin = True
            return f(*args, **kwargs)
            
        except Exception as e:
            print(f"Admin check error: {e}")
            if is_html_request:
                return redirect('/')
            return jsonify({'error': 'Authorization check failed'}), 500
    
    return decorated_function

def is_user_admin(user_id):
    # check the admins table
    try:
        result = supabase_admin.table('admins').select('*').eq('user_id', user_id).execute()
        return result.data and len(result.data) > 0
    except Exception as e:
        print(f"Admin check error: {e}")
        return False
