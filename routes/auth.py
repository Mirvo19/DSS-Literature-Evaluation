from flask import Blueprint, request, jsonify, render_template, make_response
from supabase import create_client
from config import Config
from utils.auth import is_user_admin

bp = Blueprint('auth', __name__, url_prefix='/auth')

# init supabase
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

@bp.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if response.user:
            resp_data = {
                'message': 'Signup successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email
                },
                'session': {
                    'access_token': response.session.access_token if response.session else None
                }
            }
            
            resp = make_response(jsonify(resp_data), 201)
            
            # Set cookie if session exists
            if response.session and response.session.access_token:
                resp.set_cookie(
                    'access_token',
                    response.session.access_token,
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=60*60*24*7  # 7 days
                )
            
            return resp
        else:
            return jsonify({'error': 'Signup failed'}), 400
            
    except Exception as e:
        error_message = str(e)
        if 'already registered' in error_message.lower():
            return jsonify({'error': 'Email already registered'}), 400
        elif 'password' in error_message.lower():
            return jsonify({'error': 'Password does not meet requirements'}), 400
        return jsonify({'error': f'Signup error: {error_message}'}), 400

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user and response.session:
            # check admin
            is_admin = is_user_admin(response.user.id)
            
            # Create response with cookie
            resp = make_response(jsonify({
                'message': 'Login successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email
                },
                'session': {
                    'access_token': response.session.access_token
                },
                'is_admin': is_admin
            }), 200)
            
            # Set httponly cookie for server-side auth
            resp.set_cookie(
                'access_token',
                response.session.access_token,
                httponly=True,
                secure=True,  # Only send over HTTPS
                samesite='Lax',
                max_age=60*60*24*7  # 7 days
            )
            
            return resp
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        error_message = str(e)
        if 'invalid' in error_message.lower() or 'credentials' in error_message.lower():
            return jsonify({'error': 'Invalid email or password'}), 401
        return jsonify({'error': f'Login error: {error_message}'}), 400

@bp.route('/logout', methods=['POST'])
def logout():
    # code
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
            supabase.auth.sign_out()
        
        # Clear the cookie
        resp = make_response(jsonify({'message': 'Logout successful'}), 200)
        resp.set_cookie('access_token', '', expires=0, httponly=True, secure=True, samesite='Lax')
        return resp
    except Exception as e:
        return jsonify({'error': f'Logout error: {str(e)}'}), 400

@bp.route('/verify', methods=['GET'])
def verify_token():
    # code
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        user = supabase.auth.get_user(token)
        
        if user and user.user:
            is_admin = is_user_admin(user.user.id)
            return jsonify({
                'user': {
                    'id': user.user.id,
                    'email': user.user.email
                },
                'is_admin': is_admin
            }), 200
        else:
            return jsonify({'error': 'Invalid token'}), 401
            
    except Exception as e:
        return jsonify({'error': f'Verification error: {str(e)}'}), 401
