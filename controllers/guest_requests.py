"""
# Guest Requests Controller
"""
from controllers import app, render_template
from models.guest_request import GuestRequest


#
# Home Pages
#
@app.route('/guest-requests/', methods=['GET'])
def guest_requests_index():
    guest_requests = GuestRequest.s_recently_created(100)
    return render_template('guest_requests/index.html',
                           guest_requests=guest_requests,
                           table='guest_requests/_table.html')

@app.route('/admin/guest-requests/', methods=['GET'])
def guest_requests_admin_index():
    guest_requests = GuestRequest.s_recently_created(100)
    return render_template('guest_requests/index.html',
                           guest_requests=guest_requests,
                           table='guest_requests/_admin_table.html')
