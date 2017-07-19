"""
# Guest Requests Controller
"""
from controllers import app, render_template
from models.guest_request import GuestRequest


#
# Home Pages
#
# GET /guest_requests/
@app.route('/guest-requests/', methods=['GET'])
def guest_requests_index():
    guest_requests = GuestRequest.s_recently_created(100)
    return render_template('guest_requests/index.html',
                           guest_requests=guest_requests)
