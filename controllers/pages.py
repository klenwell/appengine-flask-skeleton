"""
# Pages Controller
"""
from datetime import datetime, timedelta

from controllers import app, render_template, jsonify


#
# Home Pages
#
@app.route('/', methods=['GET'])
def pages_home():
    return render_template('pages/home.html')

#
# Admin Pages
#
@app.route('/admin/', methods=['GET'])
def pages_admin():
    return render_template('pages/admin.html')

#
# API Pages
#
@app.route('/api/ping/', methods=['GET'])
def pages_api_v1_ping():
    response = {
        'timestamp': datetime.utcnow(),
        'ping': 'pong'
    }
    return jsonify(response)
