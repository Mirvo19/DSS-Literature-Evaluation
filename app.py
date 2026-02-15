from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# routes
from routes import auth, events, admin, judge

app.register_blueprint(auth.bp)
app.register_blueprint(events.bp)
app.register_blueprint(events.api_bp)
app.register_blueprint(admin.bp)
app.register_blueprint(judge.bp)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=(app.config['ENV'] == 'development'), host='0.0.0.0', port=5000)
