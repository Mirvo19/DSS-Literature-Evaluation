from flask import Flask, render_template, send_from_directory, redirect
from flask_cors import CORS
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# api routes
from routes import auth, events, admin, judge

app.register_blueprint(auth.bp)
app.register_blueprint(events.bp)
app.register_blueprint(events.api_bp)
app.register_blueprint(admin.bp)
app.register_blueprint(judge.bp)

# page routes
from routes.en import pages as en_pages
from routes.ne import pages as ne_pages

app.register_blueprint(en_pages.bp)
app.register_blueprint(ne_pages.bp)

@app.after_request
def inject_vercel_speed_insights(response):
    """Inject Vercel Speed Insights script into every HTML page."""
    if 'text/html' in response.content_type:
        script = (
            b'\n<script>'
            b'window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };'
            b'</script>'
            b'\n<script defer src="/_vercel/speed-insights/script.js"></script>'
            b'\n</head>'
        )
        response.direct_passthrough = False
        response.data = response.data.replace(b'</head>', script, 1)
    return response

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=(app.config['ENV'] == 'development'), host='0.0.0.0', port=5000)

